#pragma once

#include "esp_camera.h"
#include "esp_err.h"

/**
 * Upload a JPEG camera frame to the Raspberry Pi.
 */
esp_err_t http_upload_frame(
    const camera_fb_t *frame
);