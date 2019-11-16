open HMG, $ARGV[0];
open DIC, "> dicts/other_omographs.dic";

$k = 0;
while(<HMG>){
	@spl = split("=", $_);
	if($spl[0] =~ m/\|\|/){
		print "$spl[0] $k\n";
		$k++;
		$flag = 1;
		$i = 0;
		while(($i <= $#readings) && !($readings[$i] eq $spl[1])){
			$i++;
		}
		if($i > $#readings){
			push(@readings, $spl[1]);
			push(@readingsNum, 1);
		} else {
			@readingsNum[$i]++;
		}
	} else {
		if($k > 0){
			$max = 0;
			for($i = 0; $i <= $#readingsNum; $i++){
				if($readingsNum[$i] > $max){
					$max = $readingsNum[$i];
					$maxInd = $i;
				} 
			}
			print DIC "\$$word=$readings[$maxInd]";
		}
		$word = $spl[0];
		@readings = ();
		@readingsNum = ();
		$k = 0;
	}
}

close DIC;
close HMG;