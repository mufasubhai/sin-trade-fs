1. Change cadence of pings. We can update to every 5 minutes for prometheus checks. ✅
2. Change the cadence of data collection. We don't need to do as frequently. Every 5 minutes should be acceptable. ✅
2. Add a prometheus check to grafana => this is basically a heartbeat to keep alive ~ 5 minutes  ✅
3. Add a prometheus check to the frontend => same ~ 5 minutes ✅
4. Add a DS heartbeat to prometheus. ~ 5 minutes ✅
5. Add testing to current functionality.
6. Add Registration Page
7. Add Charts
8. Add first draft of data service logic for calculation of alert
9. Add logic for email through supabase for alert to user. Message queue to back end, back end process message, backend send alert through supabase. 