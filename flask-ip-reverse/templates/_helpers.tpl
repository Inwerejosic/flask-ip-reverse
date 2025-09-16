{{- define "flask-ip-reverse.name" -}}
{{ .Chart.Name }}
{{- end }}

{{- define "flask-ip-reverse.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end }}

{{- define "flask-ip-reverse.chart" -}}
{{ .Chart.Name }}-{{ .Chart.Version }}
{{- end }}
