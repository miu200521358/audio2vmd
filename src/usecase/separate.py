import datetime
import os
import pathlib
import shutil

from spleeter.audio import Codec
from spleeter.audio.adapter import AudioAdapter
from spleeter.separator import Separator

from mlib.base.exception import MLibException
from mlib.base.logger import MLogger

import warnings

warnings.filterwarnings("ignore")

logger = MLogger(__name__)
__ = logger.get_text


class AudioSeparator:
    @staticmethod
    def execute(args):
        logger.info("音声分離 準備開始", decoration=MLogger.Decoration.BOX)

        if not os.path.exists(args.audio_path):
            logger.error("指定された音声ファイルパスが存在しません\n{a}", a=args.audio_path, decoration=MLogger.Decoration.BOX)
            raise MLibException("not found audio file")

        try:
            # 親パス(指定がなければ動画のある場所。Colabはローカルで作成するので指定あり想定)
            base_dir = str(pathlib.Path(args.audio_path).parent) if not args.parent_dir else args.parent_dir

            if len(args.parent_dir) > 0:
                process_audio_dir = base_dir
            else:
                process_audio_dir = os.path.join(
                    base_dir, "{0}_{1:%Y%m%d_%H%M%S}".format(os.path.basename(args.audio_path).replace(".", "_"), datetime.datetime.now())
                )

            # 既存は削除
            if os.path.exists(process_audio_dir):
                shutil.rmtree(process_audio_dir)

            # フォルダ生成
            os.makedirs(process_audio_dir)

            audio_adapter = AudioAdapter.default()
            waveform, sample_rate = audio_adapter.load(args.audio_path)

            # 音声と曲に分離
            separator = Separator("spleeter:2stems")

            # Perform the separation
            prediction = separator.separate(waveform)

            # 音声データ
            vocals = prediction["vocals"]

            vocals_wav_path = f"{process_audio_dir}/vocals.wav"

            # 一旦wavとして保存
            audio_adapter.save(vocals_wav_path, vocals, sample_rate, Codec.WAV)

            logger.info("音声分離 処理終了: {d}", d=process_audio_dir, decoration=MLogger.Decoration.BOX)

            return True, process_audio_dir
        except Exception as e:
            logger.critical("音声分離で予期せぬエラーが発生しました。", e, decoration=MLogger.Decoration.BOX)
            return False, None
