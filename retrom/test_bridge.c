#include <assert.h>
#include "bridge.c"

static retro_environment_t host_environment;
static retro_video_refresh_t host_video;
static retro_audio_sample_batch_t host_audio;
static retro_input_state_t host_input;
static unsigned runs, unloads;
void retro_set_environment(retro_environment_t cb) { host_environment = cb; }
void retro_set_video_refresh(retro_video_refresh_t cb) { host_video = cb; }
void retro_set_audio_sample(retro_audio_sample_t cb) { (void)cb; }
void retro_set_audio_sample_batch(retro_audio_sample_batch_t cb) { host_audio = cb; }
void retro_set_input_poll(retro_input_poll_t cb) { (void)cb; }
void retro_set_input_state(retro_input_state_t cb) { host_input = cb; }
void retro_init(void) {}
void retro_deinit(void) {}
void retro_unload_game(void) { unloads++; }
bool retro_load_game(const struct retro_game_info *game) {
    const char *save = NULL;
    assert(host_environment(RETRO_ENVIRONMENT_GET_SAVE_DIRECTORY, &save));
    assert(strcmp(save, "/save") == 0);
    return strcmp(game->path, "/game/Doukutsu.exe") == 0;
}
void retro_set_controller_port_device(unsigned port, unsigned device) {
    assert(port == 0 && device == RETRO_DEVICE_JOYPAD);
}
void retro_get_system_av_info(struct retro_system_av_info *av) { av->timing.fps = 60; }
void retro_run(void) {
    uint16_t frame[] = {0xf800, 0x07e0, 0x001f, 0xffff};
    int16_t sound[] = {123, -123, 456, -456};
    host_video(frame, 2, 2, 4); host_audio(sound, 2); runs++;
}
int main(void) {
    assert(retrom_step(0, 0) == 0);
    assert(retrom_load("/invalid") == 0 && !retrom_ready());
    assert(retrom_load("/game/Doukutsu.exe") == 1 && retrom_ready());
    assert(runs == 1 && retrom_width() == 2 && retrom_height() == 2);
    const uint8_t *rgba = retrom_pixels();
    assert(rgba[0] == 255 && rgba[1] == 0 && rgba[2] == 0 && rgba[3] == 255);
    assert(rgba[4] == 0 && rgba[5] == 255 && rgba[6] == 0);
    assert(retrom_step(1 << RETRO_DEVICE_ID_JOYPAD_RIGHT, 0) == 1);
    assert(host_input(0, RETRO_DEVICE_JOYPAD, 0, RETRO_DEVICE_ID_JOYPAD_RIGHT) == 1);
    assert(host_input(0, RETRO_DEVICE_JOYPAD, 0, RETRO_DEVICE_ID_JOYPAD_A) == 0);
    assert(retrom_audio_count() == 4 && ((int16_t *)retrom_audio())[1] == -123);
    retrom_step(0, 0);
    assert(host_input(0, RETRO_DEVICE_JOYPAD, 0, RETRO_DEVICE_ID_JOYPAD_RIGHT) == 0);
    retrom_stop(); retrom_stop();
    assert(unloads == 1 && retrom_step(0xffff, 0xffff) == 0);
    return 0;
}
