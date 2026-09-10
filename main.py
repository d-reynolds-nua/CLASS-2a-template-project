"""Wires the audio pipeline and rendering engine together and runs the app.

ENGINE and AUDIO_FILE are fixed, version-controlled choices, not runtime
options — committing to one engine tier and one audio file is a project
decision, not something to toggle per run.
"""

from audio.pipeline import AudioPipeline
from engines.base_engine import BaseEngine
from engines.modern_gl_engine import ModernGLEngine
from engines.pygame_engine import PygameEngine
from engines.pyglet_engine import PygletEngine

# Set this to whichever engine tier your project uses. See the README for
# how/why this is a one-time project decision, not a runtime toggle.
ENGINE: type[BaseEngine] = PygameEngine

AUDIO_FILE = "audio/track.wav"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "BSP2a Project"
TARGET_FPS = 60


def run_engine_only() -> None:
    """Runs the chosen engine with no audio pipeline involved.

    Use this to confirm your engine opens a window and closes cleanly
    before AudioPipeline is implemented — see the README.
    """
    engine = ENGINE(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    engine.run(feature_source=lambda: {})


def run_full_app():
    engine = ENGINE(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, title=WINDOW_TITLE, target_fps=TARGET_FPS)

    pipeline = AudioPipeline(file_path=AUDIO_FILE)
    try:
        pipeline.load()
        feature_source = pipeline.get_features
    except NotImplementedError:
        print("AudioPipeline not implemented yet -- running with a blank feature source.")
        feature_source = lambda: {}

    engine.run(feature_source=feature_source)


if __name__ == "__main__":
    run_full_app()
