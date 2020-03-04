Vue.config.devtools = true;
var app = new Vue({
    el: '#vueApp',
    delimiters: ['{[', ']}'],
    data: {
        message: 'Wait while we load your products ...',
        brands: [],
        checkedBrands: [],
        categories: [],
        category: '',
        products: [],
        search: '',
        page: 1,
        pages: 1
    },
    created: function() {
        this.category = this.getParam('category');
        this.getAllProducts(this.category, this.checkedBrands , this.search, this.page)
    },
    methods: {
        searchProducts: function(event){
            setTimeout(() => {
               this.search = event.target.value;
               this.getAllProducts(this.category, this.checkedBrands , this.search, this.page);
               this.search = '';
            }, 2000);
        },
        getAllProducts: function(category = this.category, brands = this.checkedBrands, search = this.search, page = this.page) {
            let endpoint = document.querySelector("#productsUrl").getAttribute("data-url"),
                params  = { category: category, brands: brands , search: search, page: page},
                _data = {};
                console.log(params);
            axios.get(endpoint, { params: params })
            .then(res =>  {
                this.products = res.data.products
                this.brands = res.data.brands
                this.categories = res.data.categories
                this.pages = res.data.pages
            })
            .catch(err => { console.log("error", err) })
        },
        getParam: function(param){
            return new URLSearchParams(window.location.search).get(param);
        },
        categoryFilter: function(event){
            this.category = event.target.attributes['data-category'].value;
            this.getAllProducts(this.category, this.checkedBrands, this.search, this.page);
            // set active
            document.querySelectorAll('.category-links.active').forEach(category => { category.className = 'category-links' })
            event.target.className = 'category-links active';
        },
        brandsFilter: function(event){
            setTimeout(() => {
                this.getAllProducts(this.category, this.checkedBrands, this.search, this.page);
              }, 1000);
        },
        pagenateProducts: function(event) {
            this.page = event.target.attributes['data-page'].value * 1;
            this.getAllProducts(this.category, this.checkedBrands, this.search, this.page);
            this.page = 1
        }
    }
})