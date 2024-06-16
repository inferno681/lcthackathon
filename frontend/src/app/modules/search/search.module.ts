import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { StoreModule } from '@ngrx/store';
import { EffectsModule } from '@ngrx/effects';

import { SearchRoutingModule } from './search-routing.module'
import { SharedModule } from '../../shared/shared.module';

import { SearchFeatureName } from './state/selectors';
import * as reducer from './state/reducers';

import { CreateStorageProviders } from '../../shared/services';
import { SearchService } from './services';

import { PAGES } from './pages';
import { COMPONENTS } from './components';
import { EFFECTS } from './state/effects';

const stateConfig = CreateStorageProviders<reducer.SearchState>('Search', SearchFeatureName, []);

@NgModule({
    declarations: [
        ...PAGES,
        ...COMPONENTS
    ],
    exports: [],
    imports: [
        CommonModule,
        SearchRoutingModule,
        EffectsModule.forFeature(EFFECTS),
        StoreModule.forFeature(SearchFeatureName, reducer.reducer, stateConfig.config),
        SharedModule
    ],
    providers: [
        SearchService,
        ...stateConfig.providers
    ]
})
export class SearchModule { }