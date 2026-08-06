#pragma once

#include "esp_err.h"

/**
 * @brief Initialize the ESP32 in Wi-Fi station mode and
 * connect to the configured wireless network.
 *
 * @return ESP_OK if the connection succeeds,
 * otherwise an ESP-IDF error code.
 */
esp_err_t wifi_init_sta();

/**
 * @brief Check whether the ESP32 is currently connected
 * to the Wi-Fi network.
 *
 * @return true if connected.
 * @return false otherwise.
 */
bool wifi_is_connected();