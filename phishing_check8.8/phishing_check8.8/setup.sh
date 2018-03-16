#!/bin/sh    
if [ $1 = 'start' ];then
	if [ $2 = 'all' ];then
		cd domain
		python DomainEngine.py start
		cd ..
		cd filtrate
		python FiltrateEngine.py start
		cd ..
		cd metasearching
		python MetasearchingEngine.py start 
		cd ..
		cd qt_crawler
		python QtCrawlerEngine.py start
		cd ..
		cd structure
		python StructureEngine.py start
		cd ..
		cd title
		python TitleEngine.py start
		cd ..
		cd web_save
		python WebSaveEngine.py start
		cd ..
		cd main_control
		python Maincontrol.py start
		cd ..
		cd view_collect
		python ViewCollectEngine.py start
		cd ..
		cd view_emd
		python ViewEmdEngine.py start
		cd ..
		cd feature_save
		python FeatureSaveEngine.py start
		cd ..
		cd whois_search
		python WhoisSearchEngine.py start
		cd ..

	else
		case  $2  in 
			"domain")
		cd domain
		python DomainEngine.py start
		cd .. 
		;;
		"filtrate")
		cd filtrate
		python FiltrateEngine.py start
		cd ..
		;;
		"metasearching")
		cd metasearching
		python MetasearchingEngine.py start 
		cd ..
		;;
		"qt_crawler")
		cd qt_crawler
		python QtCrawlerEngine.py start
		cd ..
		;;
		"structure")
		cd structure
		python StructureEngine.py start
		cd ..
		;;
		"title")
		cd title
		python TitleEngine.py start
		cd ..
		;;
		"web_save")
		cd web_save
		python WebSaveEngine.py start
		cd ..
		;;
		"main_control")
		cd main_control
		python Maincontrol.py start
		cd ..
		;;
		"feature_save")
		cd feature_save
		python FeatureSaveEngine start
		cd ..
		;;
		"whois_search")
		cd whois_search
		python WhoisSearchEngine start
		cd ..
		;;
		"view_collect")
		cd view_collect
		python ViewCollectEngine start
		cd ..
		;;
		"view_emd")
		cd view_emd
		python ViewEmdEngine start
		cd ..
		;;
		esac
	fi
elif [ $1 = 'stop' ]; then
	if [ $2 = 'all' ];then
		cd domain
		python DomainEngine.py stop
		cd ..
		cd filtrate
		python FiltrateEngine.py stop
		cd ..
		cd metasearching
		python MetasearchingEngine.py stop 
		cd ..
		cd qt_crawler
		python QtCrawlerEngine.py stop
		cd ..
		cd structure
		python StructureEngine.py stop
		cd ..
		cd title
		python TitleEngine.py stop
		cd ..
		cd web_save
		python WebSaveEngine.py stop
		cd ..
		cd main_control
		python Maincontrol.py stop
		cd ..
		cd view_collect
		python ViewCollectEngine.py stop
		cd ..
		cd view_emd
		python ViewEmdEngine.py stop
		cd ..
		cd feature_save
		python FeatureSaveEngine.py stop
		cd ..
		cd whois_search
		python WhoisSearchEngine.py stop
		cd ..

	else
		case  $2  in 
			"domain")
		cd domain
		python DomainEngine.py stop
		cd .. 
		;;
		"filtrate")
		cd filtrate
		python FiltrateEngine.py stop
		cd ..
		;;
		"metasearching")
		cd metasearching
		python MetasearchingEngine.py stop 
		cd ..
		;;
		"qt_crawler")
		cd qt_crawler
		python QtCrawlerEngine.py stop
		cd ..
		;;
		"structure")
		cd structure
		python StructureEngine.py stop
		cd ..
		;;
		"title")
		cd title
		python TitleEngine.py stop
		cd ..
		;;
		"web_save")
		cd web_save
		python WebSaveEngine.py stop
		cd ..
		;;
		"main_control")
		cd main_control
		python Maincontrol.py stop
		cd ..
		;;
		"feature_save")
		cd feature_save
		python FeatureSaveEngine stop
		cd ..
		;;
		"whois_search")
		cd whois_search
		python WhoisSearchEngine stop
		cd ..
		;;
		"view_collect")
		cd view_collect
		python ViewCollectEngine stop
		cd ..
		;;
		"view_emd")
		cd view_emd
		python ViewEmdEngine stop
		cd ..
		;;
		esac
	fi

elif [ $1 = 'restart' ]; then
	if [ $2 = 'all' ];then
		cd domain
		python DomainEngine.py restart
		cd ..
		cd filtrate
		python FiltrateEngine.py restart
		cd ..
		cd metasearching
		python MetasearchingEngine.py restart 
		cd ..
		cd qt_crawler
		python QtCrawlerEngine.py restart
		cd ..
		cd structure
		python StructureEngine.py restart
		cd ..
		cd title
		python TitleEngine.py restart
		cd ..
		cd web_save
		python WebSaveEngine.py restart
		cd ..
		cd main_control
		python Maincontrol.py restart
		cd ..
		cd view_collect
		python ViewCollectEngine.py restart
		cd ..
		cd view_emd
		python ViewEmdEngine.py restart
		cd ..
		cd feature_save
		python FeatureSaveEngine.py restart
		cd ..
		cd whois_search
		python WhoisSearchEngine.py restart
		cd ..
	else
		case  $2  in 
			"domain")
		cd domain
		python DomainEngine.py restart
		cd .. 
		;;
		"filtrate")
		cd filtrate
		python FiltrateEngine.py restart
		cd ..
		;;
		"metasearching")
		cd metasearching
		python MetasearchingEngine.py restart 
		cd ..
		;;
		"qt_crawler")
		cd qt_crawler
		python QtCrawlerEngine.py restart
		cd ..
		;;
		"structure")
		cd structure
		python StructureEngine.py restart
		cd ..
		;;
		"title")
		cd title
		python TitleEngine.py restart
		cd ..
		;;
		"web_save")
		cd web_save
		python WebSaveEngine.py restart
		cd ..
		;;
		"main_control")
		cd main_control
		python Maincontrol.py restart
		cd ..
		;;
		"feature_save")
		cd feature_save
		python FeatureSaveEngine restart
		cd ..
		;;
		"whois_search")
		cd whois_search
		python WhoisSearchEngine restart
		cd ..
		;;
		"view_collect")
		cd view_collect
		python ViewCollectEngine restart
		cd ..
		;;
		"view_emd")
		cd view_emd
		python ViewEmdEngine restart
		cd ..
		;;
		esac
	fi

else
	echo 'NO this param'
fi
