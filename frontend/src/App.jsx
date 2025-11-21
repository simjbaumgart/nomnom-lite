import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, CircleMarker, Circle } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default marker icons in React-Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

function App() {
  const mapRef = useRef(null);
  const [weather, setWeather] = useState(null);
  const [cafes, setCafes] = useState([]);
  const [hotspots, setHotspots] = useState([]);
  const [activityZones, setActivityZones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadingScored, setLoadingScored] = useState(false);
  const [error, setError] = useState(null);
  const [showControls, setShowControls] = useState(false);
  const [showTop15, setShowTop15] = useState(true);
  const [showPermitInfo, setShowPermitInfo] = useState(false);
  const [permitInfo, setPermitInfo] = useState(null);
  const [permitFilter, setPermitFilter] = useState('all'); // 'all', 'green', 'yellow', 'red' 
  const [showZones, setShowZones] = useState(true);
  const [showHotspots, setShowHotspots] = useState(true);
  const [events, setEvents] = useState([]);
  const [showEvents, setShowEvents] = useState(true);

  // Filter states
  const [minTraffic, setMinTraffic] = useState(0);
  const [maxCompetition, setMaxCompetition] = useState(2000);
  const [requireSuitableWeather, setRequireSuitableWeather] = useState(false);
  const [useLiveData, setUseLiveData] = useState(false);
  const [simulatedHour, setSimulatedHour] = useState(new Date().getHours());

  useEffect(() => {
    fetchInitialData();
    fetchPermitInfo();
  }, []);

  const fetchInitialData = async () => {
    try {
      setLoading(true);

      // Fetch weather
      const weatherRes = await fetch(`${API_BASE_URL}/api/weather`);
      const weatherData = await weatherRes.json();
      setWeather(weatherData);

      // Fetch cafes
      const cafesRes = await fetch(`${API_BASE_URL}/api/cafes`);
      const cafesData = await cafesRes.json();
      setCafes(cafesData);

      // Fetch scored hotspots and zones
      await fetchScoredData();

      // Fetch events
      const eventsRes = await fetch(`${API_BASE_URL}/api/events`);
      const eventsData = await eventsRes.json();
      setEvents(eventsData);

      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };


  const fetchPermitInfo = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/permit-info`);
      const data = await res.json();
      setPermitInfo(data);
    } catch (err) {
      console.error('Failed to fetch permit info:', err);
    }
  };

  const fetchScoredData = async () => {
    try {
      setLoadingScored(true);

      const params = new URLSearchParams({
        min_traffic: minTraffic,
        max_competition_distance: maxCompetition,
        require_suitable_weather: requireSuitableWeather,
        use_live_data: useLiveData,
        simulated_hour: simulatedHour
      });

      // Fetch hotspots
      const scoredRes = await fetch(`${API_BASE_URL}/api/hotspots-scored?${params}`);
      const scoredData = await scoredRes.json();
      setHotspots(scoredData);

      // Fetch activity zones
      const zonesRes = await fetch(`${API_BASE_URL}/api/activity-zones?${params}`);
      const zonesData = await zonesRes.json();
      setActivityZones(zonesData);

      setLoadingScored(false);
    } catch (err) {
      setError(err.message);
      setLoadingScored(false);
    }
  };

  const applyFilters = () => {
    fetchScoredData();
  };

  const flyToSpot = (lat, lon) => {
    if (mapRef.current) {
      mapRef.current.flyTo([lat, lon], 15, { duration: 1.5 });
    }
  };

  // Copenhagen coordinates
  const position = [55.6761, 12.5683];

  // Custom icon for hotspots
  const hotspotIcon = new L.divIcon({
    className: 'custom-marker hotspot-marker',
    html: '⭐',
    iconSize: [30, 30],
  });

  // Custom icon for events
  const eventIcon = new L.divIcon({
    className: 'custom-marker event-marker',
    html: '🎪',
    iconSize: [35, 35],
  });

  // Custom icon for cafes
  const cafeIcon = new L.divIcon({
    className: 'custom-marker cafe-marker',
    html: '☕',
    iconSize: [30, 30],
  });


  // Filter hotspots by permit status
  const filteredHotspots = hotspots.filter(spot => {
    if (permitFilter === 'all') return true;
    return spot.permit_status === permitFilter;
  });

  // Get top 15 from filtered spots
  const top15Spots = filteredHotspots.slice(0, 15);


  return (
    <div className="app">
      <header className="header">
        <h1>☕ NomNom Lite</h1>
        <div className="weather-info">
          {weather && !weather.error && (
            <>
              <div className="weather-item">
                <span className="weather-label">Temperature</span>
                <span className="weather-value">{weather.temperature}°C</span>
              </div>
              <div className="weather-item">
                <span className="weather-label">Wind Speed</span>
                <span className="weather-value">{weather.wind_speed} km/h</span>
              </div>
              <div className="weather-item">
                <span className="weather-label">Conditions</span>
                <span className={`weather-value ${weather.is_suitable ? 'weather-suitable' : 'weather-unsuitable'}`}>
                  {weather.is_suitable ? '✓ Suitable' : '✗ Poor'}
                </span>
              </div>
            </>
          )}
          <button
            className="control-toggle-btn"
            onClick={() => setShowControls(!showControls)}
          >
            {showControls ? '✕ Hide Filters' : '⚙️ Show Filters'}
          </button>
          <button
            className="top15-toggle-btn"
            onClick={() => setShowTop15(!showTop15)}
          >
            {showTop15 ? '✕ Hide Top 15' : '🏆 Show Top 15'}
          </button>
        </div>
      </header>

      {showControls && (
        <div className="control-panel">
          <div className="control-section">
            <h3>Business Score Filters</h3>
            <div className="control-row">
              <label>
                <span className="control-label">Min Traffic Level: {minTraffic}%</span>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={minTraffic}
                  onChange={(e) => setMinTraffic(Number(e.target.value))}
                  className="slider"
                />
              </label>
            </div>
            <div className="control-row">
              <label>
                <span className="control-label">Max Competition Distance: {maxCompetition}m</span>
                <input
                  type="range"
                  min="0"
                  max="2000"
                  step="50"
                  value={maxCompetition}
                  onChange={(e) => setMaxCompetition(Number(e.target.value))}
                  className="slider"
                />
              </label>
            </div>
            <div className="control-row">
              <label className="toggle-label">
                <input
                  type="checkbox"
                  checked={requireSuitableWeather}
                  onChange={(e) => setRequireSuitableWeather(e.target.checked)}
                />
                <span>Only show weather-suitable spots</span>
              </label>
            </div>
            <div className="control-row">
              <label>
                <span className="control-label">Simulated Hour: {simulatedHour}:00</span>
                <input
                  type="range"
                  min="0"
                  max="23"
                  value={simulatedHour}
                  onChange={(e) => setSimulatedHour(Number(e.target.value))}
                  className="slider"
                />
              </label>
            </div>
            <div className="control-row">
              <label className="toggle-label">
                <input
                  type="checkbox"
                  checked={useLiveData}
                  onChange={(e) => setUseLiveData(e.target.checked)}
                />
                <span>Use live Popular Times data (slow)</span>
              </label>
            </div>
            <div className="control-row">
              <label className="control-label">Permit Zone Restriction</label>
              <div className="permit-filter-group">
                <button
                  className={`permit-btn ${permitFilter === 'all' ? 'active' : ''}`}
                  onClick={() => setPermitFilter('all')}
                >
                  All Zones
                </button>
                <button
                  className={`permit-btn permit-green ${permitFilter === 'green' ? 'active' : ''}`}
                  onClick={() => setPermitFilter('green')}
                  title="Easy to get permit"
                >
                  Green
                </button>
                <button
                  className={`permit-btn permit-yellow ${permitFilter === 'yellow' ? 'active' : ''}`}
                  onClick={() => setPermitFilter('yellow')}
                  title="Moderate restrictions"
                >
                  Yellow
                </button>
                <button
                  className={`permit-btn permit-red ${permitFilter === 'red' ? 'active' : ''}`}
                  onClick={() => setPermitFilter('red')}
                  title="Restricted / Difficult"
                >
                  Red
                </button>
              </div>
            </div>
            <div className="control-row">
              <button
                className="info-btn"
                onClick={() => setShowPermitInfo(true)}
              >
                ℹ️ View Permit Regulations
              </button>
            </div>
            <div className="control-row">
              <label className="toggle-label">
                <input
                  type="checkbox"
                  checked={showZones}
                  onChange={(e) => setShowZones(e.target.checked)}
                />
                <span>Show Activity Zones</span>
              </label>
            </div>
            <div className="control-row">
              <label className="toggle-label">
                <input
                  type="checkbox"
                  checked={showHotspots}
                  onChange={(e) => setShowHotspots(e.target.checked)}
                />
                <span>Show Individual Hotspots</span>
              </label>
            </div>
            <div className="control-row">
              <label className="toggle-label">
                <input
                  type="checkbox"
                  checked={showEvents}
                  onChange={(e) => setShowEvents(e.target.checked)}
                />
                <span>Show Events (Daily Scrape)</span>
              </label>
            </div>
            <button
              className="apply-filters-btn"
              onClick={applyFilters}
              disabled={loadingScored}
            >
              {loadingScored ? '⏳ Loading...' : '✓ Apply Filters'}
            </button>
            <div className="info-text">
              {activityZones.length} zone{activityZones.length !== 1 ? 's' : ''}, {filteredHotspots.length} spot{hotspots.length !== 1 ? 's' : ''}
            </div>
          </div>

          <div className="legend-section">
            <h3>Business Score Legend</h3>
            <div className="legend-item">
              <div className="legend-color" style={{ backgroundColor: '#22c55e' }}></div>
              <span>Excellent (80-100)</span>
            </div>
            <div className="legend-item">
              <div className="legend-color" style={{ backgroundColor: '#eab308' }}></div>
              <span>Good (60-79)</span>
            </div>
            <div className="legend-item">
              <div className="legend-color" style={{ backgroundColor: '#f59e0b' }}></div>
              <span>Moderate (40-59)</span>
            </div>
            <div className="legend-item">
              <div className="legend-color" style={{ backgroundColor: '#ef4444' }}></div>
              <span>Poor (0-39)</span>
            </div>
          </div>
        </div>
      )}

      {showTop15 && (
        <div className="top15-sidebar">
          <h3>🏆 Top 15 Best Spots</h3>
          <div className="top15-list">
            {top15Spots.map((spot, index) => (
              <div
                key={`top15-${index}`}
                className="top15-item"
                onClick={() => flyToSpot(spot.lat, spot.lon)}
              >
                <div className="top15-rank" style={{ backgroundColor: spot.color }}>
                  #{index + 1}
                </div>
                <div className="top15-info">
                  <div className="top15-name">{spot.name}</div>
                  <div className="top15-score" style={{ color: spot.color }}>
                    ★ {spot.business_score}/100
                  </div>
                  <div className="top15-details">
                    👥 {spot.traffic_level}% • ☕ {spot.nearest_cafe_distance}m
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className={`map-container ${showTop15 ? 'with-sidebar' : ''}`}>
        {loading ? (
          <div className="loading">Loading Copenhagen map data...</div>
        ) : error ? (
          <div className="error">Error: {error}</div>
        ) : (
          <MapContainer
            center={position}
            zoom={13}
            style={{ height: '100%', width: '100%' }}
            ref={mapRef}
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            {/* Activity Zones (Large Aggregated Areas) */}
            {showZones && activityZones.map((zone, index) => (
              <Circle
                key={`zone-${index}`}
                center={[zone.center_lat, zone.center_lon]}
                radius={zone.radius}
                pathOptions={{
                  fillColor: zone.color,
                  fillOpacity: 0.15,
                  color: zone.color,
                  weight: 3,
                  opacity: 0.6,
                }}
              >
                <Popup>
                  <div className="popup-content">
                    <strong>📍 {zone.name}</strong>
                    <div className="popup-score" style={{ color: zone.color }}>
                      ★ Avg Business Score: {zone.avg_business_score}/100
                    </div>
                    <div className="popup-details">
                      <div>👥 Avg Traffic: {zone.avg_traffic}%</div>
                      <div>☕ Avg Competition: {zone.avg_competition_distance}m</div>
                      <div>📊 Hotspots in zone: {zone.hotspot_count}</div>
                    </div>
                    <div className="popup-recommendation">
                      {zone.recommendation.toUpperCase()} ZONE
                    </div>
                  </div>
                </Popup>
              </Circle>
            ))}

            {/* Individual Hotspots */}
            {showHotspots && filteredHotspots.map((spot, index) => (
              <React.Fragment key={`hotspot-${index}`}>
                <CircleMarker
                  center={[spot.lat, spot.lon]}
                  radius={spot.business_score / 5}
                  pathOptions={{
                    fillColor: spot.color,
                    fillOpacity: 0.4,
                    color: spot.color,
                    weight: 2,
                  }}
                >
                  <Popup>
                    <div className="popup-content">
                      <strong>{spot.name}</strong>
                      <div className="popup-score" style={{ color: spot.color }}>
                        ★ Business Score: {spot.business_score}/100
                      </div>
                      {spot.event_boost > 0 && (
                        <div className="popup-event-boost">
                          🔥 Traffic Boosted by Event!
                          <br />
                          <small>+{spot.event_boost}% from {spot.nearby_events[0].name}</small>
                        </div>
                      )}
                      <div className="popup-details">
                        <div>
                          👥 Traffic: {spot.traffic_level}%
                          {spot.event_boost > 0 && <span className="boost-tag">↑ Boosted</span>}
                          {spot.traffic_level < 30 && !spot.event_boost && <span className="quiet-tag"> 🌙 Quiet</span>}
                        </div>
                        <div>☕ Competition: {spot.nearest_cafe_distance}m away</div>
                        <div>🌤️ Weather: {spot.weather_suitable ? 'Suitable' : 'Unsuitable'}</div>
                        <div className="permit-status-row">
                          <span>📜 Permit: </span>
                          <span className={`permit-badge permit-${spot.permit_status}`}>
                            {spot.permit_label}
                          </span>
                        </div>
                      </div>
                      <div className="popup-recommendation">
                        {spot.recommendation.toUpperCase()} OPPORTUNITY
                      </div>
                    </div>
                  </Popup>
                </CircleMarker>
                <Marker position={[spot.lat, spot.lon]} icon={hotspotIcon}>
                  <Popup>
                    <div className="popup-content">
                      <strong>{spot.name}</strong>
                      <div className="popup-score" style={{ color: spot.color }}>
                        ★ {spot.business_score}/100
                      </div>
                      <div className="permit-status-row-small">
                        <span className={`permit-dot permit-${spot.permit_status}`}></span>
                        {spot.permit_label}
                      </div>
                    </div>
                  </Popup>
                </Marker>
              </React.Fragment>
            ))}

            {/* Events */}
            {showEvents && events.map((event) => (
              <Marker key={`event-${event.id}`} position={[event.lat, event.lon]} icon={eventIcon}>
                <Popup>
                  <div className="popup-content">
                    <strong>🎪 {event.name}</strong>
                    <p>{event.description}</p>
                    <div className="popup-details">
                      <div>📍 Impact Radius: {event.impact_radius}m</div>
                      <div>📈 Traffic Boost: +{event.traffic_boost}%</div>
                    </div>
                  </div>
                </Popup>
              </Marker>
            ))}

            {/* Cafes (Competitors) */}
            {cafes.slice(0, 100).map((cafe) => (
              !cafe.error && (
                <Marker key={`cafe-${cafe.id}`} position={[cafe.lat, cafe.lon]} icon={cafeIcon}>
                  <Popup>
                    <strong>{cafe.name}</strong>
                    <br />
                    <em>☕ Competitor</em>
                  </Popup>
                </Marker>
              )
            ))}
          </MapContainer>
        )}
      </div>
      {showPermitInfo && permitInfo && (
        <div className="modal-overlay" onClick={() => setShowPermitInfo(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h2>📜 Copenhagen Street Trading Permits</h2>
              <button className="close-btn" onClick={() => setShowPermitInfo(false)}>✕</button>
            </div>
            <div className="modal-body">
              <div className="permit-section">
                <h3>General Rules</h3>
                <ul>
                  {permitInfo.general_rules.map((rule, i) => (
                    <li key={i}>{rule}</li>
                  ))}
                </ul>
              </div>

              <div className="permit-zones">
                <h3>Zone Classifications</h3>

                <div className="zone-card green">
                  <h4>🟢 Green Zones (Easy)</h4>
                  <p><strong>Locations:</strong> {permitInfo.zones.green.locations.join(', ')}</p>
                  <p><strong>Requirements:</strong> {permitInfo.zones.green.requirements}</p>
                  <p><strong>Cost:</strong> {permitInfo.zones.green.cost}</p>
                </div>

                <div className="zone-card yellow">
                  <h4>🟡 Yellow Zones (Moderate)</h4>
                  <p><strong>Locations:</strong> {permitInfo.zones.yellow.locations.join(', ')}</p>
                  <p><strong>Requirements:</strong> {permitInfo.zones.yellow.requirements}</p>
                  <p><strong>Cost:</strong> {permitInfo.zones.yellow.cost}</p>
                </div>

                <div className="zone-card red">
                  <h4>🔴 Red Zones (Restricted)</h4>
                  <p><strong>Locations:</strong> {permitInfo.zones.red.locations.join(', ')}</p>
                  <p><strong>Requirements:</strong> {permitInfo.zones.red.requirements}</p>
                  <p><strong>Cost:</strong> {permitInfo.zones.red.cost}</p>
                </div>
              </div>
            </div>
            <div className="modal-footer">
              <p className="disclaimer"><small>{permitInfo.disclaimer}</small></p>
              <p><a href={permitInfo.application_url} target="_blank" rel="noopener noreferrer">Source: City of Copenhagen</a></p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
