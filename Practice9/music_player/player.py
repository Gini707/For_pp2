import os
import pygame


class MusicPlayer:
    def __init__(self, playlist):
        self.playlist = playlist
        self.current_index = 0
        self.is_playing = False
        self.is_stopped = True
        self.track_start_time = 0

        if self.playlist:
            self.load_track(self.current_index)

    def load_track(self, index):
        if not self.playlist:
            return

        self.current_index = index % len(self.playlist)
        pygame.mixer.music.load(self.playlist[self.current_index])
        self.track_start_time = 0

    def play(self):
        if not self.playlist:
            return

        pygame.mixer.music.play()
        self.is_playing = True
        self.is_stopped = False
        self.track_start_time = pygame.time.get_ticks()

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_stopped = True
        self.track_start_time = 0

    def next_track(self):
        if not self.playlist:
            return

        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.load_track(self.current_index)
        self.play()

    def previous_track(self):
        if not self.playlist:
            return

        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.load_track(self.current_index)
        self.play()

    def get_current_track_name(self):
        if not self.playlist:
            return "No tracks found"
        return os.path.basename(self.playlist[self.current_index])

    def get_status(self):
        if self.is_playing:
            return "Playing"
        if self.is_stopped:
            return "Stopped"
        return "Paused"

    def get_elapsed_seconds(self):
        if not self.is_playing:
            return 0
        return (pygame.time.get_ticks() - self.track_start_time) // 1000