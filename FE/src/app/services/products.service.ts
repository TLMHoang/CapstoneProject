import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { AuthService } from './auth.service';
import { environment } from 'src/environments/environment';

export class Product {
  id: number;
  name: string;
  imeis: string[]
  countSerial: number | null | undefined;

  constructor() {
    this.id = -1
    this.name = ''
    this.imeis = []
    this.countSerial = 0
  }

  init(obj?: any) {
    if (obj) {
      this.id = obj["id"];
      this.name = obj["name"];
    }
  }
}

@Injectable({
  providedIn: 'root'
})
export class ProductsService {

  url = environment.apiServerUrl;

  public items: { [key: number]: Product } = {};

  constructor(private auth: AuthService, private http: HttpClient) { }

  getHeaders() {
    const header = {
      headers: new HttpHeaders()
        .set('Authorization', `Bearer ${this.auth.activeJWT()}`)
    };
    return header;
  }

  getProducts(isDetails: boolean = false) {
    // if (this.auth.can('get:products-detail') && isDetails) {
    //   this.http.get(this.url + '/products-detail', this.getHeaders())
    //   .subscribe((res: any) => {
    //     this.productsToItems(res.products);
    //     console.log(res);
    //   });
    // } else {
    this.http.get(this.url + '/products', this.getHeaders())
      .subscribe((res: any) => {
        this.productsToItems(res.products);
        console.log(res);
      });
    // }
  }

  getProductDetail(product: Product, productId: number) {
    this.http.get(this.url + `/products/${productId}`, this.getHeaders())
      .subscribe(res => {
        let imeis = res["serials"] as string[]
        product.imeis = imeis
        product.countSerial = imeis.length
      })
  }

  saveProduct(product: Product) {
    if (product.id >= 0) { // patch
      this.http.patch(this.url + '/products/' + product.id, product, this.getHeaders())
        .subscribe((res: any) => {
          if (res.success) {
            this.productsToItems(res.products);
          }
        });
    } else { // insert
      this.http.post(this.url + '/CreateProducts', product, this.getHeaders())
        .subscribe((res: any) => {
          if (res.success) {
            this.productsToItems(res.products);
          }
        });
    }

  }

  deleteProduct(product: Product) {
    delete this.items[product.id];
    this.http.delete(this.url + '/products/' + product.id, this.getHeaders())
      .subscribe((res: any) => {

      });
  }

  productsToItems(products: Array<Product>) {
    for (const product of products) {
      this.items[product.id] = product;
    }
  }
}
