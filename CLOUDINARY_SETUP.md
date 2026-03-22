# Cloudinary Storage Setup Guide

Your Django resort website has been configured to use **Cloudinary** for all media storage instead of Railway's persistent volume.

## What Changed

✅ Added `cloudinary` and `django-cloudinary-storage` packages to `requirements.txt`  
✅ Updated Django settings to use Cloudinary as the default file storage  
✅ Removed Railway-specific local volume storage configuration  
✅ Added Cloudinary environment variables to `.env.example`

## Setup Instructions

### 1. Create a Cloudinary Account

If you don't have one:
- Go to [cloudinary.com](https://cloudinary.com/)
- Sign up for a free account
- Free tier includes 25GB storage and 25GB monthly transformations

### 2. Get Your Credentials

1. Log in to [Cloudinary Console](https://console.cloudinary.com/)
2. Navigate to **Settings → General** tab
3. You'll see:
   - **Cloud Name** (required)
   - **API Key** (required)
   - **API Secret** (keep this private!)

### 3. Update Your Environment File

Create a `.env` file in the project root based on `.env.example`:

```bash
# Copy the example file
cp .env.example .env
```

Add your Cloudinary credentials to `.env`:

```env
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

Or if already in a virtual environment:

```bash
pip install cloudinary django-cloudinary-storage
```

### 5. Verify Configuration

Your Django settings now include:
- `DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'`
- Cloudinary library is configured in `INSTALLED_APPS`

### 6. Automatic Image Compression

✨ **NEW**: The system automatically compresses large images before upload!

- **Free tier limit**: 10MB per file
- **Auto compression**: Images exceeding this size are automatically compressed
- **How it works**: 
  - Admin uploads an image > 10MB
  - System automatically compresses it to ~9MB
  - Maintains quality while staying within limits
  - No manual action needed!

**Compression happens for**:
- All model image uploads (Rooms, Blog Posts, Gallery, Hero slides, etc.)
- Any ImageField in any model
- Both admin and programmatic uploads

### 7. Test Image Uploads

Upload a test image through Django Admin:
1. Run `python manage.py runserver`
2. Go to `/admin/`
3. Add a new item with an image (e.g., Room, Review, Blog Post)
4. Images should upload directly to Cloudinary (auto-compressed if needed)
5. Check your [Cloudinary Media Library](https://console.cloudinary.com/media_library) to confirm

## Important Notes

⚠️ **Never commit your `.env` file** to version control  
⚠️ **Keep your API Secret private** - treat it like a password  
⚠️ **For Railway deployment**, add the Cloudinary credentials as environment variables in Railway dashboard:
   - Go to your Railway project settings
   - Add the three Cloudinary environment variables

## Migrating Existing Images to Cloudinary

If you already have images stored locally (in `/media/` folder), use the migration scripts:

### Option 1: Simple Migration (Recommended)

```bash
# Compresses large images and uploads all to Cloudinary
python migrate_images.py
```

This script:
- ✅ Finds all images in `/media/` folder
- ✅ Auto-compresses any files larger than 10MB
- ✅ Uploads everything to Cloudinary
- ✅ Shows progress and any errors

### Option 2: Compress First (If needed)

```bash
# Only compress images, don't upload
python compress_images.py

# Then upload manually
python migrate_images.py
```

### Results

After migration, images are:
- ✅ Stored in Cloudinary (not on server)
- ✅ Served via CDN
- ✅ Automatically optimized
- 🗑️ Local `/media/` folder can be deleted/ignored

---

## Troubleshooting

### Images Not Uploading?
- Verify credentials in `.env` are correct
- Check that `CLOUDINARY_STORAGE` settings in `settings.py` are properly configured
- Ensure all three credentials (CLOUD_NAME, API_KEY, API_SECRET) are set

### Still seeing local uploads?
- Make sure you ran `pip install -r requirements.txt`
- Restart your Django development server
- Clear any cached imports

### Image Too Large?
- Automatic compression handles files up to 10MB
- If an image still fails, try manually compressing with `compress_images.py`

## Benefits of Cloudinary

✅ Auto image optimization  
✅ CDN delivery (global distribution)  
✅ Responsive image transformations  
✅ No server storage needed  
✅ Automatic backups  
✅ Easy scaling  

## Next Steps for Railway Deployment

If deploying to Railway:
1. Go to your Railway project dashboard
2. Click on your app
3. Go to **Variables**
4. Add three new variables:
   - `CLOUDINARY_CLOUD_NAME`
   - `CLOUDINARY_API_KEY`
   - `CLOUDINARY_API_SECRET`
5. Deploy your updated code

Your site is now ready to use Cloudinary storage! 🚀
