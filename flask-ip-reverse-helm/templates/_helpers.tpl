{{- define "flask-ip-reverse.name" -}}
{{ .Chart.Name }}
{{- end }}

{{- define "flask-ip-reverse.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | replace "." "-" | trunc 63 | trimSuffix "-" -}}
{{- end }}
