{{- define "flask-ip-reverse.name" -}}
{{ .Chart.Name }}
{{- end }}

{{- define "flask-ip-reverse.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | replace "." "-" | trunc 63 | trimSuffix "-" -}}
{{- end }}

# Turning it off

# gcloud container clusters resize flask-devops-gke \
#     --node-pool default-pool \
#     --num-nodes 0 \
#     --zone us-central1

# Turning it on

# gcloud container clusters resize flask-devops-gke \
#     --node-pool default-pool \
#     --num-nodes 1 \
#     --zone us-central1



http://104.154.171.70:3000/d/85a562078cdf77779eaa1add43ccec1e/kubernetes-compute-resources-namespace-pods?orgId=1&refresh=10s

http://34.57.32.31:5000/

