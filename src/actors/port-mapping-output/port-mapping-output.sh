$LEAPP_ACTOR_OUTPUT '[{{range $index, $element := .exposed_ports.ports}}{{if $index}},{{end}}[{{$element.exposed_port}}, {{$element.port}}]{{end}}]'
