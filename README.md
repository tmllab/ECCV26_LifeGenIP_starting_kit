# LifeGenIP @ ECCV 2026 — Starting Kit

**Competition: Unlearnable Videos against Diffusion-based Customization**

[![Workshop](https://img.shields.io/badge/Workshop-Homepage-green)](https://lifegenip.cc)
[![Competition](https://img.shields.io/badge/Competition-Homepage-brightgreen)](https://lifegenip.cc/competition)
[![Codabench](https://img.shields.io/badge/Codabench-Submit-yellowgreen)](https://www.codabench.org/competitions/16817/)
[![Discord](https://img.shields.io/badge/Discord-Join-5865F2?logo=discord&logoColor=white)](https://discord.gg/vvF9zsTcZ)
[![WeChat](https://img.shields.io/badge/WeChat-Group-07C160?logo=wechat&logoColor=white)](https://lifegenip.cc/wechat)

## About the Challenge

### Background

With recent advances in diffusion-based video generation, anyone can now synthesize high-quality video content from minimal input. This creates serious threats to facial privacy: a malicious actor can collect publicly available clips of a target person and generate misleading or harmful content about them, from fake news to violations of portrait rights. Protecting video content from such misuse has become a pressing concern.

Current video customization tools follow two paradigms. **Tuning-based methods** fine-tune a video diffusion model (e.g., via LoRA) on a small set of clips of the target person and then generate diverse new videos from text prompts. **Reference-based methods**, such as image-to-video (I2V) models, take a single reference image plus a text prompt and synthesize a clip. Both pathways enable identity misuse. However, video-level protection has received much less attention than image protection. Defenses against tuning-based customization of video diffusion models remain largely unexplored, while existing work mostly targets image-domain editing or reference-based I2V threats.

### Task

Participants design a *protection* method that perturbs face-centric video clips. Protection succeeds when the customized output either does not reproduce the target identity or does not follow the attacker's text prompt.

### Threat Model

Two attack pathways:

- **Reference-based (I2V).** The attacker samples a single random frame from a protected clip and feeds it together with a text prompt to an I2V model to synthesize a short video. The attack succeeds if the generated video reproduces the target identity and follows the prompt.
- **Tuning-based.** The attacker uses the entire set of protected clips for one identity to fine-tune a video diffusion model via Low-Rank Adaptation (LoRA). The customized model is then prompted to generate new videos. The attack succeeds if the generated videos reproduce the target identity and follow the prompts.

### Evaluation Tracks

- **Effectiveness** measures how strongly the protection breaks customization on the known model. Each protected clip is fed directly into the customization pipeline against the known model.
- **Robustness** measures whether the protection survives attacks that exploit inter-frame relationships. The protected video is first passed through a hidden temporal attack (e.g., temporal averaging) before being used for customization against the known model.
- **Transferability** measures whether the protection generalizes beyond the known model. Submissions are evaluated against hidden video diffusion models.

### Phases

- **Phase 1 — Preliminary** (open to all teams). Tests the reference-based (I2V) threat. Scored on **Effectiveness** and **Robustness**. Top teams advance to Phase 2.  👉 For details on environment setup, model, data download, hardware requirements, running example, evaluation, and submission, see: **[`phase1/README.md`](phase1/README.md).**
- **Phase 2 — Final** (top teams from Phase 1). Tests both reference-based (I2V) and tuning-based threats. Scored on all three tracks. Starting kit will be released later.

Important dates and deadlines: please see the [codabench timeline page](https://www.codabench.org/competitions/16817/). 


## Rules

⚠️ Participating teams must not target or attack the hidden evaluation metrics or scoring models. Such behavior may compromise the fairness of the competition and lead to misleadingly high scores without providing video protection capability.

During the competition, submissions will be reviewed through both automated checks and manual inspection. Suspicious submissions may be placed on hold or rejected.

**In addition, before the final round, qualifying teams must submit reproducible code for review. Violation of the rules may result in disqualification.**

## Registration and Submission

Participate by submit a [Google form](https://forms.gle/UkgYXdFbPGrSafoP7) and register on our Codabench competition page:

**https://www.codabench.org/competitions/16817/**

There you can register and join this competition, make your submissions, and track your rank on the live leaderboard. 

> Phase 1 closes on **July 15** (AOE time). You may register and submit at any time before the deadline.

## License

This competition uses [MEAD dataset](https://wywu.github.io/projects/MEAD/MEAD.html) with the authors' permission. By downloading the data you agree to the MEAD [Terms of Use](https://github.com/uniBruce/Mead/blob/master/Terms%20of%20Use_%20Mead.pdf). Any report or publication that uses this data **should cite** the MEAD paper: 

```bibtex
@inproceedings{kaisiyuan2020mead,
  author    = {Wang, Kaisiyuan and Wu, Qianyi and Song, Linsen and Yang, Zhuoqian and Wu, Wayne and Qian, Chen and He, Ran and Qiao, Yu and Loy, Chen Change},
  title     = {MEAD: A Large-scale Audio-visual Dataset for Emotional Talking-face Generation},
  booktitle = {ECCV},
  month     = {August},
  year      = {2020}
}
```

Code in this repository is released under [Apache License 2.0](LICENSE).

The motivation, problem formulation, analysis of video-specific temporal challenges, and unified evaluation suite that form the basis of this competition are presented in the following paper. If you use the competition benchmark, evaluation suite, or starting kit in your research, please consider citing it:

```bibtex
@article{huang2026delving,
  title={Delving into the Temporal Challenges of Unified Video Protection Against Image-to-Video and Fine-Tuning-based Customization},
  author={Yuxin Huang and Ziming Hong and Mingming Gong and Wanyu Wang and Jing Zhang and Tongliang Liu},
  year={2026},
  journal={arXiv preprint arXiv:2607.13336}
}
```

## Contact

For competition-related questions, technical issues, or bug reports, you can contact us via:

* [Email](mailto:lifegenip_workshop@googlegroups.com)
* [WeChat Group](https://lifegenip.cc/wechat)
* [Discord Server](https://discord.gg/vvF9zsTcZ)
* [Codabench Forum](https://www.codabench.org/forums/16538/)
