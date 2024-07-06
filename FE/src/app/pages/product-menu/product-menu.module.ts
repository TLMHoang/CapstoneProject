import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';

import { IonicModule } from '@ionic/angular';

import { ProductMenuPage } from './product-menu.page';
import { ProductFormComponent } from './product-form/product-form.component';

const routes: Routes = [
  {
    path: '',
    component: ProductMenuPage
  }
];

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    RouterModule.forChild(routes)
  ],
  entryComponents: [ProductFormComponent],
  declarations: [ProductMenuPage, ProductFormComponent],
})
export class ProductMenuPageModule {}
