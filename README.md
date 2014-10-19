# FlowReader Semantics

- App: http://flow-semantics.appspot.com/
- Info: https://github.com/hackathonBI/Flowreader

## Work In Progress:

- [x] Connect to BigQuery from local dev server using [client ID](https://stackoverflow.com/questions/20349189/unable-to-access-bigquery-from-local-app-engine-development-server/22723127#22723127) created on BigQuery project.
- [x] Connect to BigQuery from App Engine cloud using App Enging [service account](https://cloud.google.com/bigquery/authorization#service-accounts-appengine) added to BigQuery project.
- [x] Get Flowreader dataset source table rows.
- [ ] Create task queue to query Semantria API and insert extended records to new table.
- [ ] Report/queue records that are not extended, or were removed.
- [ ] Add basic frontend sync controls (admin account only).
