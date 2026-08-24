---
name: free-gpu
description: 無料の計算資源（Kaggle Notebooks GPU/TPU、Google Colab 無料枠、ローカル GPU/MPS/CPU）で学習を回す方法と使い分け。GPU が必要なモデル（NN・大規模学習）を訓練したいときに使用。
---

# Free GPU Training — 無料資源だけで回す

このテンプレートは **有償のGPUレンタル（vast.ai / RunPod 等）や有償APIを前提にしない** 構成を標準としています。
主に次の3つを活用します。

| 資源 | 上限 | 得意 | 制約 |
|------|------|------|------|
| **Kaggle Notebooks** | GPU 約30h/週、TPU 約20h/週、1セッション最大12h（変動あり） | 中〜大規模NN、大規模CV | ネット遮断モードあり、データはKaggle Datasets経由 |
| **Google Colab 無料枠** | 不定（混雑で割当なしもある）、アイドル切断あり | 単発実験・短い学習 | 予告なく切断。長時間学習は不可 |
| **ローカル (CUDA / MPS / CPU)** | 無制限 | GBDT、中小規模NN、特徴量作成 | マシンスペック依存 |

## 使い分け

```
GBDT（LightGBM/XGBoost/CatBoost）      → ローカルCPU/GPUで十分。
表形式NN / MLP                          → ローカル (CUDA / MPS / CPU)
大規模NN / 画像・テキスト事前学習        → Kaggle Notebooks GPU
最終アンサンブル・stacking               → ローカル（軽い）
```

## Kaggle GPU で回す

1. 学習スクリプトを notebook 化して `kernel-metadata.json` を用意する。
2. `kaggle-notebooks` スキル（Kaggle MCP の `save_notebook` / `create_notebook_session`）で push & run。
3. 完了後 `download_notebook_output` で OOF / test 予測を取得し、`data/processed/preds/` に置く。
4. ローカルのベースラインモデルとまとめて blend / stacking する。

GPU クォータは `mcp__kaggle__get_accelerator_quota` で確認できる。週の残量を見てから長い学習を投げる。

### Kaggle GPU 利用時の注意

- **コンペ規約を確認**: 配布データの外部持ち出しが禁止されているコンペ（SIGNATE 等）では、
  そのデータを Kaggle Datasets にアップロードしてはいけない。その場合はローカル or Colab で回す。
- 1セッションの上限（〜12h）を超える学習は、fold 単位で分割して複数回に分ける。
- 出力は `/kaggle/working/` に書く。20GB 制限。
- インターネット無効のコンペでは、依存パッケージも Dataset 経由で持ち込む。

## Colab 無料枠

- 「短い実験を1本だけ試す」用途に限る。学習途中でランタイムが切れる前提で、
  **必ず fold ごとにチェックポイントを Google Drive か Kaggle Dataset に保存**する。
- 長時間学習の本命にしない（切断で全部失う）。

## ローカル実行時のデバイス選択

```python
import torch

device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
```

- PyTorch コードでは `cuda` > `mps` > `cpu` の順に自動検出する構成を標準とする。
- macOS (Apple Silicon MPS) で非対応演算に当たった場合は `PYTORCH_ENABLE_MPS_FALLBACK=1` を設定可能。

## やらないこと

- 有償GPUレンタル（vast.ai / RunPod / Lambda）、有償API（OpenAI・Perplexity 等）を前提にした手順を提案しない。
  必要になった場合は「無料枠でどこまでやれるか」を先に提示し、課金は必ずユーザーの明示的な判断に委ねる。
