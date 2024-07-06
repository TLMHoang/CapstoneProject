import { Component, OnInit, Input } from '@angular/core';
import { ModalController } from '@ionic/angular';
import { AuthService } from 'src/app/services/auth.service';
import { Product, ProductsService } from 'src/app/services/products.service';

@Component({
  selector: 'app-product-form',
  templateUrl: './product-form.component.html',
  styleUrls: ['./product-form.component.scss'],
})
export class ProductFormComponent implements OnInit {
  @Input() product: Product;
  @Input() isNew: boolean;

  constructor(
    public auth: AuthService,
    private modalCtrl: ModalController,
    private productService: ProductsService
    ) { }

  ngOnInit() {
    if (this.isNew) {
      this.product = new Product()
    }
    else{
      this.productService.getProductDetail(this.product, this.product.id);
    }
  }

  closeModal() {
    this.modalCtrl.dismiss();
  }

  saveClicked() {
    for (let i = 1; i <= 5; i++) {
      this.product.imeis.push(`${this.product.name}00000000${i}`)  
    }
    this.productService.saveProduct(this.product);
    this.closeModal();
  }

  deleteClicked() {
    this.productService.deleteProduct(this.product);
    this.closeModal();
  }
}
