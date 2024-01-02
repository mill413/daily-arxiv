# Daily Arxiv

A python script to automatically update papers daily from arxiv using Github Actions.

## Usage

1. Fork this repo
2. Check `Settings->Actions->General->Workflow permissions`, choose `Read and write permissions` and save
3. Change `GITHUB_USER_NAME` and `GITHUB_USER_EMAIL` to yours in file `.github/workflows/daily-arxiv-update.yml`
4. Change keywords in `config.toml` following given format
5. Run workflow `Update arxiv` in Actions

## Todo

- [ ] Implement code link
- [ ] Pull index.md to Github Pages
- [ ] Logging timezone
- [ ] Translation

## References

The following is a list of resources that I used as reference and inspiration.

- [cv-arxiv-daily](https://github.com/Vincentqyw/cv-arxiv-daily)
- [arxiv.py](https://github.com/lukasschwab/arxiv.py)
