import { Component, OnInit } from '@angular/core';
import { ProductsService, Product } from '../../services/products.service';
import { ModalController } from '@ionic/angular';
import { ProductFormComponent } from './product-form/product-form.component';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-product-menu',
  templateUrl: './product-menu.page.html',
  styleUrls: ['./product-menu.page.scss'],
})
export class ProductMenuPage implements OnInit {
  Object = Object;

  constructor(
    private auth: AuthService,
    private modalCtrl: ModalController,
    public products: ProductsService
    ) { }

  ngOnInit() {
    this.products.getProducts();
  }

  async openForm(activeproduct: Product = null) {
    if (!this.auth.can('get:products-detail')) {
      return;
    }

    const modal = await this.modalCtrl.create({
      component: ProductFormComponent,
      componentProps: { product: activeproduct, isNew: !activeproduct }
    });

    modal.present();
  }

}
