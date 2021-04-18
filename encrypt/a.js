function cnt(string){
    let n = 1;
    for(let i = 0;i < string.length;i++){
        if(string.charAt(i) == ',')n++;
    }
    return n;
}