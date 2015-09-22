BEGIN{
	letra_actual=65;
	contador=0;
}

/entropy/ {
	print;
}
/^[0-9]+/{
	if(contador==0){
		ip=$1;
		informacion=$2;
		probabilidad=$3;
		contador++;
	} else {
		if(informacion==$2){
			contador++;
		} else {
			if(contador==1){
				print ip, informacion, probabilidad;
			} else {
				printf "%c(%d) %s %s\n", letra_actual, contador, informacion, probabilidad;
				siguiente_letra();
			}
			ip=$1;
			informacion=$2;
			probabilidad=$3;
			contador=1;
		}
	}
}
END{
	if(contador==1){
		print ip, informacion, probabilidad;
	} else {
		printf "%c(%d) %s %s \n", letra_actual, contador, informacion, probabilidad;
	}
}
func siguiente_letra(){
	letra_actual++;
	if(letra_actual==91){
		letra_actual=97;
	}
}
