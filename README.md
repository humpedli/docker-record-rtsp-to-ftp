# Record RTSP stream to FTP with Docker

This script records a video from RTSP stream and upload it to and FTP server.

The main concept is that the camera motion script triggers the POST api of this script with config data and the script will record the remote RTSP stream and will upload the recorded video to a remote FTP server:

**POST data:**

http://<script_runner_machine_ip>:11122

```
{
	"name": "<camera_name>",
	"duration": 10,
	"stream_url": "rtsp://<ip>:8554/unicast",
	"ftp_url": "ftp://<ftp_user>:<ftp_pass>@<ftp_ip>/<ftp_dir>"
}
```
**Example motion sh script for Xiaomi Dafang camera:**

More info: https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/blob/master/integration/custom/motiondetection.md

```
if [ "$1" == "on" ]; then

	source /system/sdcard/config/motion.conf
	source /system/sdcard/scripts/common_functions.sh

	$state = $(/system/sdcard/bin/curl -s -X GET \
    	-H "Authorization: Bearer <long_life_token>" \
    	-H "Content-Type: application/json" \
    	http://<homeassistant_ip>:8123/api/states/<entity_id> | jq -r '.state' 2>/dev/null)

	if [ "$state" == "on" ] ; then
		/system/sdcard/bin/curl -s -X POST \
		-H "Content-Type: application/json" \
		--data '{"name": "<camera_name>", "duration": 10, "stream_url": "rtsp://<ip>:8554/unicast", "ftp_url": "ftp://<ftp_user>:<ftp_pass>@<ftp_ip>/<ftp_dir>"}' \
		http://<script_runner_machine_ip>:11122 2>/dev/null
	fi

fi
```