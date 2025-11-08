# Operations Runbook

Use this runbook when supporting production or long-running lab deployments.

## Health Checks

| Check | Command/Endpoint | Expected Result |
| --- | --- | --- |
| API heartbeat | `curl https://<host>/health` | `{"message":"Welcome to the HoppyBrew API","status":"online"}` |
| Logs | `curl https://<host>/logs?limit=200` | JSON array of structured log entries |
| HomeAssistant summary | `curl https://<host>/homeassistant/summary` | Active batch counts, last brew timestamp |
| Docker | `docker ps` / `docker-compose ps` | `backend`, `frontend`, and `db` containers healthy |

## Routine Tasks

1. **Daily** – Review `/logs` for WARN/ERROR entries, confirm HomeAssistant sensors are updating.
2. **Weekly** – `pg_dump` the `hoppybrew_db` database and rotate Cloudflare tunnel credentials.
3. **Monthly** – Apply dependency updates (`pip`, `yarn`), regenerate diagrams, and refresh BJCP styles via `/refresh-beer-styles` endpoint.

## Incident Response

| Symptom | Actions |
| --- | --- |
| API 5xx responses | Check docker logs, inspect `logs` endpoint, confirm Postgres connectivity (`pg_isready`). Restart backend container if necessary. |
| Missing recipes/batches | Validate migrations ran; check `alembic_version` table. Restore from last backup if data corruption suspected. |
| HomeAssistant stale data | Verify backend reachable from HA instance, flush HA REST sensor cache, and confirm `/homeassistant/batches` returns JSON. |
| PlantUML render failures | Usually due to nested `@startuml`; edit source `.puml` or split diagrams. |

## Backups

```bash
# Ad-hoc backup
docker exec hoppybrew-db pg_dump -U postgres hoppybrew_db > backups/hoppybrew_$(date +%F).sql
```

- Store SQL dumps off-site; combine with Unraid snapshotting if available.
- Test restores quarterly on a staging environment.

## Upgrades

1. Pull latest code (`git pull`).
2. Rebuild images (`docker-compose build --pull`).
3. Apply migrations (`docker exec hoppybrew-backend alembic upgrade head`).
4. Run smoke tests (API `/health`, HomeAssistant summary, UI navigation).
5. Update this wiki if architecture/API/DB changes occurred.

## Observability Roadmap

- Publish Prometheus metrics from FastAPI (Starlette middleware) and Postgres exporter.
- Ship logs to Loki/ELK instead of relying solely on `/logs`.
- Add alerting via HomeAssistant automations (notify when active batches > threshold, fermentation temperature drift, etc.).
