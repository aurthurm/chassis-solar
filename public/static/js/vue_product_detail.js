
var app = new Vue({
    el: '#vueApp',
    delimiters: ['{[', ']}'],
    data: {
        message: 'Wait while we load your product detail ...',
        brands: [],
        categories: [],
        product: {
            'name': '',
            'sku': '',
            'product_id': '',
            'price': '',
            'old_price': '',
            'images0': '',
            'images1': '',
            'images2': '',
            'images3': '',
            'images4': '',
        },
    },
    created: function() {
        this.getProduct()
    },
    methods: {
        getProduct: function() {
            let endpoint = document.querySelector("#productUrl").getAttribute("data-url"),
                params  = {},
                _data = {};
            
            axios.get(endpoint, { params: params })
            .then(res =>  {
                this.product = res.data
            })
            .catch(err => { console.log("error", err) })
        },
        productImager: function(image='') {
            return 'here am i working'  + image
        }
    }
})

Vue.config.devtools = true;