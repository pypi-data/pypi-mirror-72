# Arcane bing

This package is based on [bingads](https://docs.microsoft.com/en-us/advertising/guides/request-download-report?view=bingads-13).

## Get Started

```sh
pip install arcane-bing
```

## Example Usage

```python
bing_client = Client(
    credentials=Config.BING_ADS_CREDENTIALS,
    secrets_bucket=Config.SECRETS_BUCKET,
    refresh_token_location=Config.BING_ADS_REFRESH_TOKEN,
    storage_client=storage_client
)

reporting_service_manager, reporting_service = bing_client.get_bing_ads_api_client()

report_request = build_campaigns_report(reporting_service, bing_account_id)

result_file_path = bing_client.submit_and_download(report_request, reporting_service_manager)
```
