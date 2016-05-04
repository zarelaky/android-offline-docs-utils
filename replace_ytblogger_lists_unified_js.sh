
target=ytblogger_lists_unified.js
grep -r $target|awk -F\: '{ print $1; }' > .l
for i in `cat .l`;
do
    case i in 
        $target)
            continue;;
    esac
    sed -i "s#<script.*$target.*</script>##g" $i;
done
rm .l
