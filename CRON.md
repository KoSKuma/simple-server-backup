# Delete files older than 31 days

```cron
0 0 * * * find /path/to/your/directory -type f -mtime +31 -exec rm -f {} \;
```
