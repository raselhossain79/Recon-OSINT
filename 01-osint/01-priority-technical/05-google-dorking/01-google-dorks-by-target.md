# Google Dorks by Target Category

> **Note:** Replace `{target}` with actual domain. Always verify target is in scope before running.

---

## 1. Subdomain & Asset Discovery

### Basic Subdomain Enumeration
```
site:*.{target}                         # All subdomains
site:*.{target} -www                    # Exclude www
site:*.{target} inurl:admin             # Admin on any subdomain
site:*.{target} inurl:api               # API subdomains
site:*.{target} inurl:staging           # Staging environments
site:*.{target} inurl:dev               # Development subdomains
site:*.{target} inurl:test              # Test environments
site:*.{target} inurl:internal          # Internal-facing
site:*.{target} inurl:vpn               # VPN portal
site:*.{target} inurl:remote            # Remote access
```

### Service-Specific Subdomains
```
site:*.{target} inurl:mail              # Mail servers
site:*.{target} inurl:ftp               # FTP servers
site:*.{target} inurl:chat              # Chat/Slack-like
site:*.{target} inurl:wiki              # Wiki/documentation
site:*.{target} inurl:git               # Git repositories
site:*.{target} inurl:jenkins           # CI/CD pipelines
site:*.{target} inurl:grafana           # Monitoring dashboards
site:*.{target} inurl:kibana            # Log aggregation
site:*.{target} inurl:prometheus        # Metrics
site:*.{target} inurl:sonarqube         # Code quality
site:*.{target} inurl:vault             # Password managers
site:*.{target} inurl:ldap              # Directory services
```

### Cloud & Hosted Services
```
site:*.{target} intext:"powered by AWS"
site:*.{target} intext:"Azure"
site:*.{target} intext:"Google Cloud"
site:*.{target} inurl:cdn               # CDN endpoints
site:*.{target} inurl:s3                # S3-like storage
site:*.{target} inurl:blob              # Azure Blob storage
site:*.{target} inurl:storage           # Generic storage
```

---

## 2. Exposed Configuration & Environment Files

### Direct File Search
```
site:{target} filetype:env              # .env files
site:{target} ".env" intext:"KEY"       # .env with keys
site:{target} filetype:conf             # .conf files
site:{target} filetype:config           # .config files
site:{target} filetype:ini              # .ini files
site:{target} filetype:xml              # XML configs
site:{target} filetype:json intext:"api_key"  # JSON with secrets
site:{target} filetype:yaml             # YAML configs
site:{target} filetype:properties       # Java properties
site:{target} filetype:settings         # Settings files
```

### Path-Based Search
```
site:{target} inurl:.env
site:{target} inurl:config.php
site:{target} inurl:settings.json
site:{target} inurl:application.properties
site:{target} inurl:web.config          # IIS config
site:{target} inurl:web.xml             # Tomcat config
site:{target} inurl:/etc/                # *nix configs
site:{target} inurl:var/www             # Web root configs
```

### Environment Variable Leaks
```
intext:"DB_HOST=" filetype:env
intext:"DB_PASSWORD=" filetype:env
intext:"API_KEY=" filetype:env
intext:"STRIPE_SECRET=" filetype:env
intext:"TWILIO_AUTH_TOKEN=" filetype:env
intext:"SLACK_BOT_TOKEN=" filetype:env
intext:"AWS_ACCESS_KEY" filetype:env
intext:"PRIVATE_KEY" filetype:env
site:{target} intext:"DATABASE_URL"
site:{target} intext:"REDIS_URL"
site:{target} intext:"MONGODB_URI"
```

---

## 3. Exposed Credentials & Secrets

### Generic Credential Patterns
```
intext:"username=" intext:"password=" filetype:txt
intext:"username:" intext:"password:" filetype:log
intext:"login=" intext:"pass=" filetype:conf
intext:"user=" intext:"pass=" filetype:ini
intext:"admin" intext:"pass" filetype:sql
```

### Database Credentials
```
intext:"mysql_user" intext:"mysql_password"
intext:"DB_USER" intext:"DB_PASS"
intext:"database_username" intext:"database_password"
intext:"dbuser" intext:"dbpass"
site:{target} intext:"root" intext:"password" filetype:sql
```

### API Keys & Tokens
```
intext:"api_key" filetype:js
intext:"API_KEY=" site:{target}
intext:"api_secret" filetype:json
intext:"x-api-key:" site:{target}
intext:"Bearer " filetype:js           # Auth tokens
intext:"Authorization: " filetype:log
```

### SSH Keys & Certificates
```
intext:"BEGIN PRIVATE KEY" filetype:pem
intext:"BEGIN RSA PRIVATE KEY"
intext:"-----BEGIN OPENSSH PRIVATE KEY-----"
intext:"-----BEGIN PRIVATE KEY-----"
site:{target} intext:"PRIVATE KEY"
site:{target} filetype:key
```

### Service-Specific Secrets
```
intext:"STRIPE_SECRET_KEY" filetype:env
intext:"SLACK_BOT_TOKEN" filetype:env
intext:"GITHUB_TOKEN" filetype:env
intext:"DOCKER_PASSWORD" filetype:env
intext:"AWS_SECRET_ACCESS_KEY" filetype:env
intext:"GCP_SERVICE_ACCOUNT_KEY" filetype:json
intext:"AZURE_STORAGE_KEY" filetype:env
```

### Git & Version Control
```
site:{target} filetype:git
site:{target} inurl:.git/config
intext:"git@github.com" filetype:log
intext:"Deploy key" filetype:txt
site:{target} inurl:.gitignore
site:{target} inurl:.git/HEAD
```

---

## 4. Backup & Archive Files

### SQL Dumps
```
site:{target} filetype:sql              # SQL databases
site:{target} filetype:sql.bak          # Backup databases
inurl:backup filetype:sql
inurl:database filetype:sql
inurl:dump filetype:sql
inurl:export filetype:sql
ext:sql.bak
ext:sql.gz
```

### Compressed Archives
```
site:{target} filetype:zip
site:{target} filetype:rar
site:{target} filetype:7z
site:{target} filetype:tar
inurl:backup filetype:zip
inurl:backup filetype:tar.gz
inurl:archive filetype:gz
ext:tar.gz
ext:backup.zip
```

### Backup File Extensions
```
site:{target} filetype:bak
site:{target} filetype:old
site:{target} filetype:backup
site:{target} ext:~
site:{target} ext:swp
site:{target} ext:tmp
inurl:backup filetype:bak
inurl:.backup
```

### Application-Specific Backups
```
site:{target} filetype:wpexport        # WordPress export
site:{target} filetype:joomla.sql      # Joomla backup
site:{target} filetype:drupal.sql      # Drupal backup
inurl:wp-content filetype:sql
```

---

## 5. Directory Listings & Misconfiguration

### Index Listings
```
intitle:"Index of" site:{target}        # Web server directory listing
intitle:"Directory Listing"
intitle:"Apache" filetype:html
"Parent Directory" site:{target}
"Name  Last modified"                   # Apache dir listing signature
```

### Specific Directory Exposures
```
intitle:"Index of" /admin site:{target}
intitle:"Index of" /backup site:{target}
intitle:"Index of" /upload site:{target}
intitle:"Index of" /config site:{target}
intitle:"Index of" /private site:{target}
intitle:"Index of" /secret site:{target}
intitle:"Index of" /download site:{target}
intitle:"Index of" /docs site:{target}
```

### FTP Directory Listings
```
inurl:ftp "Index of /"
inurl:ftp "drwxr-xr-x"
```

---

## 6. Debug & Error Pages

### Error Message Exposure
```
intext:"You have an error in your SQL syntax"
intext:"Warning: mysql_fetch"
intext:"Parse error:" filetype:txt
intext:"Fatal error:" filetype:log
intext:"Exception:" filetype:log
intext:"stack trace"
```

### Debug Mode Indicators
```
intitle:"Exception Details"
intitle:"Stack Trace"
intext:"debug_mode = true"
intext:"DEBUG = True"
inurl:debug filetype:log
intext:"Traceback" filetype:txt
```

### Stack Traces & Source Exposure
```
intext:"at java." filetype:txt
intext:"at com.example" filetype:log
intext:"File \"/var/" intext:"line"
intext:"Traceback (most recent call last):"
```

### Monitoring & Logging Exposure
```
intext:"Verbose mode enabled"
intitle:"Live Log"
intitle:"Request Log"
intitle:"Error Log"
site:{target} filetype:log
```

---

## 7. Login & Admin Panels

### Generic Admin Paths
```
site:{target} inurl:admin
site:{target} inurl:/login
site:{target} inurl:/signin
site:{target} inurl:/login.php
site:{target} inurl:/admin.php
site:{target} inurl:/administrator
intitle:login site:{target}
intitle:"Sign In" site:{target}
```

### CMS Admin Panels
```
site:{target} inurl:wp-admin           # WordPress
site:{target} inurl:/administrator     # Joomla
site:{target} inurl:/admin/index.php   # Drupal-like
site:{target} inurl:/typo3             # TYPO3
site:{target} inurl:/concrete5         # Concrete5
site:{target} inurl:/modx              # MODX
```

### Control Panels
```
intitle:"cPanel"
intitle:"Plesk"
intitle:"DirectAdmin"
inurl:cpanel site:{target}
inurl:plesk site:{target}
inurl:directadmin site:{target}
```

### Database Management Interfaces
```
inurl:phpmyadmin
inurl:phpPgAdmin
inurl:adminer
inurl:navicat
site:{target} inurl:phpmyadmin
site:{target} inurl:pgadmin
```

### Monitoring & Analytics Panels
```
intitle:"Dashboard"
intitle:"Admin Panel"
intitle:"Control Panel"
intitle:"Management Console"
site:{target} intitle:"dashboard"
```

---

## 8. Exposed Credentials (Lists & Databases)

### Exported User Lists
```
site:{target} filetype:xlsx intext:"username"
site:{target} filetype:csv intext:"password"
site:{target} filetype:docx intext:"credentials"
intext:"user" intext:"pass" filetype:xlsx
intext:"employee" intext:"password" filetype:csv
```

### Database Exports & Dumps
```
site:{target} filetype:sql intext:"INSERT INTO" intext:"user"
site:{target} filetype:sql intext:"CREATE TABLE" intext:"password"
intext:"INSERT INTO users" filetype:sql
intext:"INSERT INTO admin" filetype:sql
```

### Credential Stores
```
site:{target} intext:"vault" filetype:json
site:{target} intext:"credentials" filetype:txt
site:{target} intext:"password reset" filetype:log
site:{target} filetype:txt intext:"username" intext:"password"
```

---

## 9. Cloud Storage Exposure

### AWS S3 Buckets
```
site:s3.amazonaws.com
site:s3.amazonaws.com filetype:json
inurl:s3.amazonaws.com filetype:txt
"s3.amazonaws.com" filetype:pdf
bucket_name.s3.amazonaws.com           # Direct bucket URLs
s3://bucket_name                        # S3 path notation
```

### Azure Blob Storage
```
site:blob.core.windows.net
inurl:blob.core.windows.net filetype:json
"{target}.blob.core.windows.net"
```

### Google Cloud Storage
```
site:storage.googleapis.com
inurl:storage.googleapis.com
gs://{target}-bucket                    # GCS path notation
```

### DigitalOcean Spaces
```
site:nyc3.digitaloceanspaces.com
site:sfo3.digitaloceanspaces.com
```

### Exposed Object Lists
```
site:s3.amazonaws.com "Access Denied"  # Misconfigured but listed
site:s3.amazonaws.com "Index of"
site:storage.googleapis.com "Listing denied"
```

---

## 10. API Documentation & Endpoints

### Documentation Exposure
```
site:{target} inurl:/api/docs
site:{target} inurl:swagger
site:{target} inurl:swagger.json
site:{target} inurl:swagger.yaml
site:{target} inurl:/graphql
site:{target} inurl:graphiql
site:{target} inurl:postman
site:{target} inurl:api-docs
site:{target} filetype:json intext:"swagger"
site:{target} filetype:yaml intext:"openapi"
```

### API Endpoint Enumeration
```
site:{target} inurl:/api/v1
site:{target} inurl:/api/v2
site:{target} inurl:/rest/
site:{target} inurl:/api/rest
site:{target} inurl:/service
site:{target} inurl:/webservice
```

### Postman Collections
```
site:{target} filetype:json intext:"postman"
inurl:postman filetype:json
intext:"collection" filetype:json intext:"request"
```

### GraphQL Exposure
```
site:{target} inurl:graphql
site:{target} intext:"query {" filetype:json
intext:"__schema" filetype:json
```

---

## 11. Source Code Leaks

### PHP Source
```
intext:"<?php" filetype:php site:{target}
intext:"$_GET" filetype:php site:{target}
intext:"$_POST" filetype:php site:{target}
intext:"mysql_query" filetype:php
```

### JavaScript Source & Maps
```
intext:"function" filetype:js site:{target}
intext:"api_key" filetype:js site:{target}
filetype:js.map site:{target}           # Source maps with original code
```

### Python Source
```
intext:"def " filetype:py site:{target}
intext:"import" filetype:py site:{target}
filetype:py intext:"password"
```

### Java Source
```
intext:"public class" filetype:java site:{target}
intext:"@Autowired" filetype:java site:{target}
```

### Configuration as Code
```
intext:"resource" filetype:tf site:{target}  # Terraform
intext:"ansible_host" filetype:yml site:{target}  # Ansible
```

---

## 12. CI/CD & DevOps Exposure

### Jenkins
```
site:{target} inurl:jenkins
site:{target} intitle:"Jenkins"
inurl:jenkins/job/
inurl:jenkins/console
```

### GitLab CI
```
site:{target} inurl:gitlab
site:{target} inurl:.gitlab-ci.yml
site:gitlab.com/{target}
```

### GitHub Actions
```
site:github.com/{target}/.github/workflows
inurl:.github/workflows filetype:yml
```

### Docker & Container Registry
```
site:{target} inurl:docker
site:{target} inurl:registry
site:{target} intext:"Docker" inurl:build
```

### Monitoring & Observability
```
intitle:Grafana inurl:{target}
intitle:Kibana inurl:{target}
intitle:Prometheus inurl:{target}
intitle:DataDog inurl:{target}
intitle:Splunk inurl:{target}
inurl:grafana filetype:json site:{target}
```

### IaC & Infrastructure
```
site:{target} filetype:tf                # Terraform
site:{target} filetype:yml intext:"image:"  # Docker Compose
site:{target} filetype:yaml intext:"kind:"  # Kubernetes
```

---

## 13. Metadata & OSINT

### Document Metadata
```
filetype:pdf inauthor:"{target}"
filetype:docx intitle:"{target}"
filetype:xlsx site:{target}
```

### Author & Creator Info
```
inauthor:"example.com"
inauthor:"{company_name}"
```

### Wayback & Historical
```
site:{target} "2023" filetype:pdf
site:{target} "January 2024" filetype:docx
```

### Geo & Location Tags
```
intext:"{target}" intext:"office" filetype:pdf
intext:"{target}" intext:"headquarters"
```

---

## 14. Employee & Organizational Info

### Employee Directories
```
site:{target} filetype:pdf intext:"employee"
site:{target} filetype:xlsx intext:"staff"
site:{target} inurl:directory
site:{target} inurl:employees
```

### Email Addresses & Contacts
```
intext:"@{target}" filetype:pdf
intext:"@{target}" filetype:docx
site:{target} intext:"contact"
```

### Organizational Charts
```
site:{target} filetype:pdf intext:"organization"
site:{target} filetype:docx intext:"management"
```

### Job Postings (Historical)
```
site:{target} inurl:careers intext:"senior developer"
site:{target} inurl:jobs filetype:html
```

---

## 15. Vulnerable Parameter Patterns

### SQL Injection Indicators
```
site:{target} inurl:"?id="
site:{target} inurl:"?user="
site:{target} inurl:"?query="
site:{target} inurl:"?search="
intext:"You have an error in your SQL syntax"
```

### File Inclusion Vulnerability Patterns
```
site:{target} inurl:"?file="
site:{target} inurl:"?page="
site:{target} inurl:"?include="
site:{target} inurl:"?path="
```

### SSRF Patterns
```
site:{target} inurl:"?url="
site:{target} inurl:"?proxy="
site:{target} inurl:"?fetch="
```

### Open Redirect Patterns
```
site:{target} inurl:"?redirect="
site:{target} inurl:"?return="
site:{target} inurl:"?next="
site:{target} inurl:"?continue="
```

---

## 16. Third-Party & Dependency Files

### NPM Packages
```
site:{target} package.json filetype:json
site:{target} package-lock.json
```

### Python Dependencies
```
site:{target} requirements.txt
site:{target} setup.py
site:{target} Pipfile
```

### Java Dependencies
```
site:{target} pom.xml
site:{target} build.gradle
```

### Ruby Dependencies
```
site:{target} Gemfile
site:{target} Gemfile.lock
```

---

## Notes for Each Category

**Always:**
- Verify target authorization
- Check results for false positives (site: operator includes subdomains)
- Combine multiple operators for precision
- Stagger queries to avoid rate limiting
- Document findings with timestamps
- Cross-reference with other OSINT sources
