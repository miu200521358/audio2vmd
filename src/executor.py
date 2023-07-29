import argparse
import os
import time

from mlib.base.exception import MLibException
from mlib.base.logger import LoggingMode, MLogger

logger = MLogger(__name__)
__ = logger.get_text


def show_worked_time(elapsed_time: float):
    """経過秒数を時分秒に変換"""
    td_m, td_s = divmod(elapsed_time, 60)
    td_h, td_m = divmod(td_m, 60)

    if td_m == 0:
        worked_time = "00:00:{0:02d}".format(int(td_s))
    elif td_h == 0:
        worked_time = "00:{0:02d}:{1:02d}".format(int(td_m), int(td_s))
    else:
        worked_time = "{0:02d}:{1:02d}:{2:02d}".format(int(td_h), int(td_m), int(td_s))

    return worked_time


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio_path", type=str, default="", help="音声データファイルフルパス(wav, mp3)")
    parser.add_argument("--lyric_path", type=str, default="", help="歌詞データテキストファイルフルパス")
    parser.add_argument("--parent_dir", type=str, default="", help="親ディレクトリパス(Colab・ローカル切り替え用)")
    parser.add_argument("--process", type=str, default="", help="実行プロセス(カンマ区切り)")
    parser.add_argument("--verbose", type=int, default=20, help="ログレベル")
    parser.add_argument("--log_mode", type=int, default=0, help="ログ用翻訳出力モード")
    parser.add_argument("--out_log", type=bool, default=False, help="ログをファイル出力するか否か")
    parser.add_argument("--lang", type=str, default="en-us", help="言語")

    args = parser.parse_args()

    # ロガーの初期化
    MLogger.initialize(
        args.lang, os.path.dirname(os.path.abspath(__file__)), LoggingMode(args.log_mode), level=args.verbose, is_out_log=args.out_log
    )

    result = True

    start = time.time()
    logger.info("audio2vmd 実行: 処理内容: {p}", p=args.process, decoration=MLogger.Decoration.BOX)

    try:
        if "separate" in args.process:
            # 準備
            from usecase.separate import AudioSeparator

            result, args.parent_dir = AudioSeparator.execute(args)

        if "whisper" in args.process:
            # 準備
            from usecase.separate import AudioSeparator

            result, args.parent_dir = AudioSeparator.execute(args)

        # if result and "alphapose" in args.process:
        #     # alphaposeによる2D人物推定
        #     from parts.alphapose import execute

        #     result = execute(args)

        # if result and "multipose" in args.process:
        #     # MultiPoseによる人物推定
        #     from parts.multipose import execute

        #     result = execute(args)

        # if result and "posetriplet" in args.process:
        #     # posetripletによる人物推定
        #     from parts.posetriplet import execute

        #     result = execute(args)

        # if result and "mix" in args.process:
        #     # 推定結果合成
        #     from parts.mix import execute

        #     result = execute(args)

        # if result and "motion" in args.process:
        #     # モーション生成
        #     from parts.motion import execute

        #     result = execute(args)

        elapsed_time = time.time() - start

        logger.info(
            "audio2vmd 終了: 処理内容: {p}, 処理時間: {e}", p=args.process, e=show_worked_time(elapsed_time), decoration=MLogger.Decoration.BOX
        )

    except MLibException as e:
        logger.error("処理が継続できないため、中断しました\n----------------\n" + e.message, decoration=MLogger.Decoration.BOX, **e.kwargs)
    except Exception:
        logger.critical("予期せぬエラーが発生しました")
        # 例外が発生したら終了ログ出力
        logger.quit()

    finally:
        # 終了音を鳴らす
        if os.name == "nt":
            # Windows
            try:
                import winsound

                winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
            except Exception:
                pass
