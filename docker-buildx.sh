utc_time=$(date -u +"%Y-%m-%dT%H:%MZ")
latest_tag=$(git describe --tags --abbrev=0)
git_commit=$(git log --pretty=format:'%h' -n 1)
docker buildx build . -t p2f-portal:v$git_commit \
    --label "org.past2future.git-commit=$git_commit" \
    --label "org.past2future.build-time=$utc_time" \
    --label "org.opencontainers.image.created=$utc_time" \
    --label "org.opencontainers.image.version=$latest_tag-$git_commit-python3.13" 
