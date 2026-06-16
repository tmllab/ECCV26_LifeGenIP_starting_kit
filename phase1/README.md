# Phase 1: Starting Kit

This directory contains the Phase 1 starting kit. In this phase your protection is applied to a single video clip of a single identity. The threat scenario is reference-based customization: an attacker samples a random frame from the protected video clip and feeds it to an Image-to-video (I2V) model with a text prompt to generate a new video.

**Data**: Phase 1 uses face-centric video clips, 640×480, 113 frames, 1 identity, 1 clip.

**Model**: Phase 1 uses [Wan2.2-TI2V-5B](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B-Diffusers) as the video generation model.

**Perturbation Budget**: 16/255

**Evaluation Tracks**: In this phase, we evaluate each submission under two tracks:
- **Effectiveness**: the protected video clip is evaluated as-is.
- **Robustness**: the protected video clip is first processed by a temporal attack before evaluation.

## Table of Contents

- [Environment](#environment)
- [Hardware](#hardware)
- [Repository Structure](#repository-structure)
- [Data Preparation](#data-preparation)
- [How to Implement and Run a Protection Method](#how-to-implement-and-run-a-protection-method)
- [How to Evaluate](#how-to-evaluate)
- [Submission](#submission)



## Environment

Clone the repo:

```bash
git clone https://github.com/tmllab/ECCV26_LifeGenIP_starting_kit.git
cd ECCV26_LifeGenIP_starting_kit
cd phase1
```

Set up the environment:

```bash
conda create -n lifegenip python=3.10 -y
conda activate lifegenip
conda install -c conda-forge ffmpeg -y
pip install -r requirements.txt
```

Download the I2V model (~32 GB) and set `WAN_MODEL_PATH`:

```bash
huggingface-cli download Wan-AI/Wan2.2-TI2V-5B-Diffusers \
    --local-dir ./models/Wan2.2-TI2V-5B-Diffusers
export WAN_MODEL_PATH=$PWD/models/Wan2.2-TI2V-5B-Diffusers
```

## Hardware

A single NVIDIA GPU with ≥ 24 GB VRAM is recommended, e.g., RTX 3090, RTX 4090, A5000, or A6000. Tested on RTX 4090.

## Repository Structure

```
data_preparation/           # preprocess raw MEAD dataset
protect/
├── run.py                  # entry point
└── methods/
    ├── random_noise.py     # baseline: uniform L-inf noise
    └── my_method.py        # your method
eval/                       # evaluation
utils/
check_submission.py         # validate submission.zip before upload
data/
├── original/               # raw data
├── preprocessed/           # preprocessed video clips
├── protected/<method>/     # protected video clips
│   ├── submission/         # lossless, for submission
│   └── preview/            # lossy, for viewing
└── generated/<method>/     # videos generated during evaluation
```

## Data Preparation

### Download

Follow the download instructions in the [MEAD GitHub repo](https://github.com/uniBruce/Mead). The full dataset is very large (over 400 GB), so you do **not** need all of it. Phase 1 uses a single identity, so in the dataset's [Google Drive](https://github.com/uniBruce/Mead/issues/21#issuecomment-1200418970) or [Baidu Netdisk](https://github.com/uniBruce/Mead/issues/8#issuecomment-966988461) link, open the `M003` folder and download only `video.tar` from it.

> If you run into any download issues, please contact us.

### Prepare the video clips

1. Put the `video.tar` under `data/original/`:

   ```bash
   mkdir -p data/original # place video.tar at: data/original/video.tar
   ```

   > There is no need to untar `video.tar`. `preprocess.py` extracts only the required video clips automatically.

2. Verify the `video.tar` before preprocessing:

   ```bash
   python data_preparation/check.py
   ```

3. Extract and preprocess the video clips:

   ```bash
   python data_preparation/preprocess.py
   ```

   > The required raw video clips are extracted from `video.tar` automatically, saved under `data/original/<id>/`. Preprocessed video clips are written to `data/preprocessed/<id>/<vid>.mp4`.


## How to Implement and Run a Protection Method

### Run a baseline

The kit currently provides one baseline `random_noise`: uniform L∞ noise applied to every frame within the budget.

```bash
python protect/run.py --method random_noise
```

> ⚠️ Two folders are written under `data/protected/<method>/`: `submission/<id>/<vid>.mp4` (lossless) and `preview/<id>/<vid>.mp4` (lossy). The lossless mp4 is pixel-exact, but some players show it with wrong colors, so view the protected video by the `preview/` and submit the `submission/`.

### Implement your own

Edit `protect/methods/my_method.py` and implement one function:

```python
def protect(videos: dict) -> dict:
    # videos: {"front_neutral_level_1": uint8 array (113, 480, 640, 3), ...}
    #         all video clips of one identity, keyed by file name.
    # return: same keys, same shape and dtype.
    ...
```

Then run `python protect/run.py --method my_method`.

**Constraint.** Each protected video clip must satisfy `L∞ ≤ 16/255` against its original. Over-budget pixels are clipped to the budget before evaluation.

## How to Evaluate

We provide a local evaluation program against the known model ([Wan2.2-TI2V-5B](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B-Diffusers)). This program is a public reference implementation for participants to estimate methods locally. It does **not** reproduce the final leaderboard evaluation.


### Run Local Evaluation

```bash
python eval/run.py --method <method_name>
```

> Generated videos are saved to `data/generated/<method>/`, and the reference metric values are saved to `data/results_<method>.json`.

For each protected video clip, the evaluation program samples a frame from the clip and feeds it into the I2V pipeline with one public text prompt. The **protected video** and the **generated videos** is then evaluated using the metrics below.

### Metrics


| Type     | Used For                      | Evaluated On                       | What it measures                                                       | Notes                                                                |
| --------------- | -------------------------- | ---------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `face_detection`          | Effectiveness + Robustness | Generated videos                   | Face-detection failure rate (FDFR) over generated frames                      | Higher values mean better protection, indicating fewer detectable faces in the generated video. |
| `face_similarity`           | Effectiveness + Robustness | Generated videos                   | Identity similarity (ISM) between the generated face and the target identity | Lower values mean better protection. This metric is computed only on frames where a face is detected.    |
| `prompt_following` | Effectiveness + Robustness | Generated videos                   | Video-text alignment between the generated video and the text prompt   | Lower values mean better protection, indicating weaker prompt following. |
| `image_quality` | Effectiveness + Robustness | Generated videos                   | Visual quality of the generated video                                  | Lower quality means better protection, indicating lower visual quality in the generated video.   |
| `invisibility`  | Invisibility only          | Protected video | Imperceptibility of the protected video compared to the original     | Better invisibility means better invisibility. Computed once on the protected video, not on generated videos.   |

> ⚠️ Local metric values are for reference only and may not match the final leaderboard results.

Note that the `invisibility` metric is computed directly between the **protected video** clip and the **original video** clip, while all other metrics are computed based on the **generated videos**.

The final leaderboard follows the same metric types of the local evaluation program, but uses hidden text prompts, a hidden reference-frame sampling strategy, hidden face detectors and encoders (for `face_detection` and `face_similarity`), hidden vision-language models (for `prompt_following`), hidden image-quality models, and hidden temporal attacks. 

Specifically, the local evaluation program provides one public reference temporal attack for robustness evaluation. The final leaderboard evaluates robustness under **three hidden temporal attacks**.


## Submission

Build the archive from your protected output:

```bash
cd data/protected/<your_method>/submission
python -m zipfile -c ../../../../submission.zip M003
```

> `submission.zip` structure:
> ```
> submission.zip
> └── M003/
>     └── front_neutral_level_1.mp4
> ```

Before uploading, run the checker. It verifies `submission.zip` structure and every video clip uses the required lossless encoding:

```bash
cd ../../../..
python check_submission.py
```

Submissions that fail this check (wrong structure or encoding) may be rejected, to avoid evaluation issues. 

To submit, register and join our [Codabench competition](https://www.codabench.org/competitions/16817/), then upload `submission.zip` from the **My Submissions** tab.
