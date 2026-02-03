# Mouser API Fix - POST Method

## Issue
Mouser API v2 requires **POST** method, not GET.

Error: `405 - UnsupportedApiVersion - does not support HTTP method 'GET'`

## Solution Applied

Changed Mouser node to:
- **Method:** POST
- **URL:** `https://api.mouser.com/api/v2/search/keyword`
- **Body:** JSON with `SearchByKeywordRequest` object
- **API Key:** Passed as query parameter

## Mouser Node Configuration

1. **Method:** POST
2. **URL:** `https://api.mouser.com/api/v2/search/keyword`
3. **Body:**
```json
{
  "SearchByKeywordRequest": {
    "keyword": "{{ $json.keywords }}",
    "records": 5,
    "startingRecord": 0,
    "searchOptions": "",
    "searchWithYourSignUpLanguage": ""
  }
}
```
4. **Query Parameters:**
   - `apiKey` = `{{$parameter.mouserKey}}`

## Setup in n8n

1. Import updated workflow
2. Click "Mouser API Search" node
3. Add Parameter:
   - Name: `mouserKey`
   - Value: Your Mouser API key from `.env`
4. Save and test

## Test Again

Mouser API should now work! ✅
