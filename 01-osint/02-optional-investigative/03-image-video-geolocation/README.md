# Image / Video Geolocation (GEOINT)

Niche for web/API pentest work — relevant mainly for physical-security assessments or high-value social-engineering pretexting.

## Techniques

- **EXIF metadata extraction** — `exiftool image.jpg` pulls GPS coordinates (if not stripped), device model, and timestamp from publicly posted images
- **Reverse image search** — Google Images, Yandex, or TinEye to find source/original context of an image, useful for verifying whether a claimed location photo is genuine
- **Shadow/landmark/signage analysis** — manual technique for estimating location and rough time-of-day from visual cues when EXIF data has been stripped (common on social media, which re-compresses and strips metadata by default)

## When this actually matters
Only pull this technique in if the engagement explicitly includes a physical-security component (e.g., assessing whether office location/badge photos posted publicly create a physical intrusion risk). Skip entirely for standard web/API scope.
