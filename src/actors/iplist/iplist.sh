/sbin/ip -4 -o addr list | grep -E '(wl|e(th|n|m))' | sed 's/.*inet \([0-9\.]\+\)\/.*$/\1/g'
