#!/bin/bash
cd /tmp/claude-0/t
mkdir -p /tmp/claude-0/srv && ln -sfn /home/claude/pwa /tmp/claude-0/srv/dxf-viewer
(cd /tmp/claude-0/srv && python3 -m http.server 8765 >/dev/null 2>&1 &) ; sleep 1
rm -rf pf_pin pf_h2 pf_x pf_24 pf_26 pf_30a prof pf1 pf2
run(){ echo "== $1"; o=$(timeout 120 python3 $1 2>&1); c=$?; echo "$o" | grep -v -i proxy | grep -v "^- \|^(oldest\|^Allowed\|^For details\|^\s*$" | tail -${2:-4}; if [ $c -ne 0 ] || echo "$o" | grep -q "Traceback"; then echo "FAIL $1: $(echo "$o" | grep -E "Error|waiting for" | head -2 | tr '\n' ' ' | cut -c1-200)"; fi; }
run t3.py 3; run t5.py 3; run t6.py 2; run t7.py 2; run t8.py 5; run t11.py 6; run t13.py 1; run t14.py 2; run t15.py 2
run t16.py 3; run t17.py 3; run t18.py 3; run t19.py 3; run t2.py 3; run t20.py 1; run t21.py 2; run t22.py 5; run t23.py 3; run t24.py 4; run t25.py 4; run t26.py 9; run t10.py 2
run t60.py 2; run t61.py 1; run t63.py 1; run t64.py 1; run t65.py 1; run t66.py 1; run t67.py 1
run t68.py 3
run t53.py 1; run t54.py 1; run t55.py 1; run t59.py 1
pkill -f "http.server 8765"; echo DONE
