FROM debian:10

RUN	apt update && apt upgrade &&\
	apt install nginx wget git -y &&\
	apt-get install libtool autoconf build-essential libpcre3-dev zlib1g-dev libssl-dev libxml2-dev libgeoip-dev liblmdb-dev libyajl-dev libcurl4-openssl-dev libpcre++-dev pkgconf libxslt1-dev libgd-dev automake -y &&\
	apt install git -y &&\
	cd /usr/local/src &&\
	git clone --depth 100 -b v3/master --single-branch https://github.com/SpiderLabs/ModSecurity &&\
	cd ModSecurity &&\
	git submodule init &&\
	git submodule update &&\
	sh build.sh &&\
	./configure &&\
	make &&\
	make install &&\
	mkdir /usr/local/src/cpg &&\
	cd /usr/local/src/cpg &&\
	wget http://nginx.org/download/nginx-1.21.4.tar.gz &&\
	tar -xvzf nginx-1.21.4.tar.gz &&\
	git clone https://github.com/SpiderLabs/ModSecurity-nginx &&\
	cd nginx-1.21.4 &&\
	./configure --with-compat --with-openssl=/usr/include/openssl/ --add-dynamic-module=/usr/local/src/cpg/ModSecurity-nginx &&\
	make modules &&\
	cp objs/ngx_http_modsecurity_module.so /usr/share/nginx/modules/ &&\
	echo "load_module modules/ngx_http_modsecurity_module.so;" >> /etc/nginx/modules-enabled/50-mod-http-modsecurity.conf &&\
	echo "include /etc/nginx/cpguard_waf_load.conf;" >> /etc/nginx/nginx.conf &&\
	echo "modsecurity on;" >> /etc/nginx/cpguard_waf_load.conf &&\
	echo "modsecurity_rules_file /etc/nginx/nginx-modsecurity.conf;" >> /etc/nginx/cpguard_waf_load.conf &&\
	echo "SecRuleEngine On \
	SecRequestBodyAccess On \
	SecDefaultAction "phase:2,deny,log,status:406" \
	SecRequestBodyLimitAction ProcessPartial \
	SecResponseBodyLimitAction ProcessPartial \
	SecRequestBodyLimit 13107200 \
	SecRequestBodyNoFilesLimit 131072 \
	SecPcreMatchLimit 250000 \
	SecPcreMatchLimitRecursion 250000 \
	SecCollectionTimeout 600 \
	SecDebugLog /var/log/nginx/modsec_debug.log \
	SecDebugLogLevel 0 \
	SecAuditEngine RelevantOnly \
	SecAuditLog /var/log/nginx/modsec_audit.log \
	SecUploadDir /tmp \
	SecTmpDir /tmp \
	SecDataDir /tmp \
	SecTmpSaveUploadedFiles on \
	# Include file for cPGuard WAF \
	Include /etc/nginx/cpguard_waf.conf" >> /etc/nginx/nginx-modsecurity.conf 