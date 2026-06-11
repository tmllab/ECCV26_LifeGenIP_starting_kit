# LifeGenIP @ ECCV 2026 — Starting Kit

**Competition: Unlearnable Videos against Diffusion-based Customization**

[![Workshop](https://img.shields.io/badge/Workshop-Homepage-green)](https://lifegenip.cc)
[![Competition](https://img.shields.io/badge/Competition-Homepage-brightgreen)](https://lifegenip.cc/competition)
[![Codabench](https://img.shields.io/badge/Codabench-Submit-yellowgreen)](https://www.codabench.org/competitions/16817/)
[![Discord](https://img.shields.io/badge/Discord-Join-5865F2?logo=discord&logoColor=white)](https://discord.gg/vvF9zsTcZ)

> 📢 **Competition will begin on June 20th, and the starting kit will be released on June 15th.**

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

- **Phase 1 — Preliminary** (open to all teams). Tests the reference-based (I2V) threat. Scored on **Effectiveness** and **Robustness**. Top teams advance to Phase 2. **See: [`phase1/README.md`](phase1/README.md).**
- **Phase 2 — Final** (top teams from Phase 1). Tests both reference-based (I2V) and tuning-based threats. Scored on all three tracks. Starting kit released later.

Important dates and additional details: see the [official competition page](https://lifegenip.cc/competition.html).


## Contact

lifegenip_workshop@googlegroups.com
