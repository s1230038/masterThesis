NR > 1 {
    pos[1]="0";
    pos[NR]=$5;
    if ( $6=="0" || (pos[NR-1]=="0" && $6=="3") || (pos[NR-1]!="0" && $6!="3") ) {
        print $0; }
    };