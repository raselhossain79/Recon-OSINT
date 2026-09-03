# Cloud Storage Bucket Discovery

Misconfigured public buckets are one of the highest-impact, lowest-effort bug bounty findings when they exist — worth a dedicated, thorough pass rather than a quick check.

## Permutation-based discovery
Cloud storage naming is predictable enough that permutation wordlists built from the target's name reliably find real buckets:
```
cloud_enum -k targetcompany -k target -k target-prod -k target-dev --disable-azure --disable-gcp
```
`-k` accepts multiple keyword variants — always include the company name, a shortened version, and common environment suffixes (`-dev`, `-staging`, `-prod`, `-backup`).

```
python3 S3Scanner.py --list-buckets -f bucket_names_wordlist.txt
```
Build the wordlist from company-name permutations combined with common bucket-naming patterns (`target-assets`, `target-uploads`, `target-static`, `target-backups`, `target-logs`).

## Checking permissions once a bucket is found
```
aws s3 ls s3://found-bucket-name --no-sign-request
```
`--no-sign-request` tests anonymous access explicitly — a bucket listing successfully here means public read access, at minimum.

```
aws s3 cp test-file.txt s3://found-bucket-name/ --no-sign-request
```
Testing anonymous write access (use a clearly-labeled harmless test file, never anything that could be mistaken for a real upload) — public write is a more severe finding than public read.

## Indexed public buckets
GrayhatWarfare (`buckets.grayhatwarfare.com`) maintains a searchable index of already-discovered public buckets — search by the target's name as a fast complementary check alongside active permutation scanning.

## Azure Blob / GCS equivalents
```
cloud_enum -k targetcompany --disable-aws
```
Same tool, different provider flags — Azure Blob Storage and Google Cloud Storage follow similar predictable-naming patterns, worth checking regardless of which cloud provider the target's main infrastructure appears to use (multi-cloud setups are common).

## Workflow
1. Build a permutation wordlist from company name + environment suffixes
2. Run cloud_enum across AWS/Azure/GCP simultaneously
3. Cross-check GrayhatWarfare's existing index
4. For any found bucket, test anonymous read, then anonymous write, in that order
5. Never download bulk contents of a found bucket beyond what's needed to confirm the finding — record what's exposed, don't exfiltrate it

## Output
Any publicly accessible bucket is a high-priority, high-exposure asset inventory entry — flag read vs write access separately since they represent different severity levels.
