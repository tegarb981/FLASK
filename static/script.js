function konfirmasiHapus(id){
return confirm(
"Yakin ingin menghapus data buku dengan ID " +
id +
" ?"
);
}

document.addEventListener("DOMContentLoaded", function(){

```
const form = document.querySelector("form");

if(form){

    form.addEventListener("submit", function(e){

        let judul = document.querySelector(
            'input[name="judul"]'
        ).value.trim();

        let penulis = document.querySelector(
            'input[name="penulis"]'
        ).value.trim();

        let penerbit = document.querySelector(
            'input[name="penerbit"]'
        ).value.trim();

        if(
            judul === "" ||
            penulis === "" ||
            penerbit === ""
        ){
            alert("Semua field wajib diisi!");
            e.preventDefault();
        }
    });
}
```

});
