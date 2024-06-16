import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { LayoutComponent } from './layout';

import { ModulesInfo } from './modules';

export const routes: Routes = [
    {
        path: '',
        redirectTo: '/search',
        pathMatch: 'full',
    },
    {
        path: '',
        component: LayoutComponent,
        children: [
            {
                path: 'search',
                loadChildren: () => import('./modules/search/search.module').then(module => module.SearchModule),
                data: { module: ModulesInfo.search.name }
            }
        ]
    }
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }