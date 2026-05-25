#include "esp_wifi.h"
#include "esp_event.h"
#include "nvs_flash.h"
#include <math.h>

// --- Configuration ---
#define CHANNEL 3
#define WINDOW_SEC 5
#define THRESHOLD 10
#define ZSCORE_THRESHOLD 3.0
#define BASELINE_WINDOWS 12

// --- State ---
int window_count = 0;
unsigned long window_start = 0;
int total_deauths = 0;

float history[BASELINE_WINDOWS] = {0};
int history_idx = 0;
int history_filled = 0;

void wifi_sniffer_cb(void *buf, wifi_promiscuous_pkt_type_t type) {
    if (type != WIFI_PKT_MGMT) return;
    wifi_promiscuous_pkt_t *pkt = (wifi_promiscuous_pkt_t *)buf;
    uint8_t subtype = pkt->payload[0] >> 4;
    if (subtype == 0x0C || subtype == 0x0A) {
        window_count++;
        total_deauths++;
    }
}

float calc_mean(float *arr, int n) {
    float sum = 0;
    for (int i = 0; i < n; i++) sum += arr[i];
    return sum / n;
}

float calc_stddev(float *arr, int n, float m) {
    float sum = 0;
    for (int i = 0; i < n; i++) sum += (arr[i] - m) * (arr[i] - m);
    return sqrt(sum / n);
}

void check_window() {
    unsigned long now = millis();
    if (now - window_start < WINDOW_SEC * 1000) return;

    int thresh_alert = (window_count >= THRESHOLD) ? 1 : 0;
    float z = 0;
    int z_alert = 0;

    int n = history_filled ? BASELINE_WINDOWS : history_idx;
    if (n >= 3) {
        float m = calc_mean(history, n);
        float sd = calc_stddev(history, n, m);
        if (sd > 0) {
            z = (window_count - m) / sd;
            z_alert = (z > ZSCORE_THRESHOLD) ? 1 : 0;
        }
    }

    Serial.printf("%lu,%d,%d,%d,%.2f,%d\n",
                  millis(), window_count, total_deauths, thresh_alert, z, z_alert);

    history[history_idx] = window_count;
    history_idx = (history_idx + 1) % BASELINE_WINDOWS;
    if (history_idx == 0) history_filled = 1;

    window_count = 0;
    window_start = now;
}

void setup() {
    Serial.begin(115200);
    delay(1000);

    nvs_flash_init();
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    esp_wifi_init(&cfg);
    esp_wifi_set_storage(WIFI_STORAGE_RAM);
    esp_wifi_set_mode(WIFI_MODE_NULL);
    esp_wifi_start();
    esp_wifi_set_promiscuous(true);
    esp_wifi_set_promiscuous_rx_cb(&wifi_sniffer_cb);
    esp_wifi_set_channel(CHANNEL, WIFI_SECOND_CHAN_NONE);

    window_start = millis();
    Serial.println("timestamp_ms,window_deauths,total_deauths,threshold_alert,zscore,zscore_alert");
}

void loop() {
    check_window();
    delay(100);
}
