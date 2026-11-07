import argparse

from game import SpaceRocks
from storage import save_result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--player-id", type=int)
    player_id = parser.parse_args().player_id
    recorded = False

    def record(result):
        global recorded
        if player_id is not None and not recorded:
            save_result(player_id, result)
            recorded = True

    try:
        SpaceRocks(on_result=record).main_loop()
    except SystemExit:  # Esc 或关闭窗口
        record("quit")
        raise
