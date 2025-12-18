# Mapbox Token Setup Guide

## Current Token Status
Your token appears to be valid (starts with `pk.` which is correct for public tokens).

## Token Requirements for This App

For the Weather Radar app to work properly, your Mapbox token needs:

1. **Public Token** (not secret) - ✅ You have this
2. **Access to Map Styles** - Specifically `mapbox://styles/mapbox/dark-v11`
3. **No URL Restrictions** (for localhost development) OR
   - URL restrictions that include `http://localhost:3000` and `http://localhost:5173`

## How to Check/Update Your Token

1. **Go to Mapbox Account**: https://account.mapbox.com/
2. **Navigate to**: Tokens → Your token
3. **Check**:
   - Token starts with `pk.` (public) ✅
   - Scopes include: `styles:read`, `fonts:read`, `datasets:read`
   - URL restrictions (if any) include your localhost URLs

## Common Token Issues

### Issue 1: Token doesn't have style access
**Symptom**: Map loads but shows blank/gray
**Fix**: Ensure token has `styles:read` scope

### Issue 2: URL restrictions
**Symptom**: Map doesn't load, 401/403 errors
**Fix**: Add `http://localhost:3000` and `http://localhost:5173` to allowed URLs, or remove restrictions for development

### Issue 3: Token expired/revoked
**Symptom**: Map doesn't load, authentication errors
**Fix**: Create a new token

## Creating a New Token (if needed)

1. Go to https://account.mapbox.com/access-tokens/
2. Click "Create a token"
3. Name it (e.g., "Weather Radar App")
4. **Scopes**: Select:
   - ✅ `styles:read`
   - ✅ `fonts:read`
   - ✅ `datasets:read`
5. **URL restrictions**: 
   - For development: Leave empty or add `http://localhost:*`
   - For production: Add your production domain
6. Click "Create token"
7. Copy the token and update your `.env` file:
   ```
   VITE_MAPBOX_TOKEN=your_new_token_here
   ```

## Testing Your Token

Open browser console and look for:
- ✅ No errors = Token is working
- ❌ "Unauthorized" or "Invalid token" = Token issue
- ❌ "Style not found" = Token doesn't have style access

## Current Token in Use
Your token: `pk.eyJ1IjoidXNtYW5tYXFib29sOTAxIiwiYSI6ImNtamIzcHJ4bzBiaWwzZXNicXhnaDExODkifQ.vg0kYbVLLlOFaIBx1fmRQw`

If the map is loading but radar data isn't showing, the issue is likely **not** the token, but rather:
- Data format/parsing
- Heatmap layer configuration
- Backend API response

Check the browser console for specific errors to identify the issue.

