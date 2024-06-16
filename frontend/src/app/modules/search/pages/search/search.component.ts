import { Component, OnInit, OnDestroy } from '@angular/core';
import {
  AbstractControl,
  UntypedFormArray,
  FormControl,
  FormGroup,
  Validators
} from '@angular/forms';
import { Store, select } from "@ngrx/store";
import { Subscription, isEmpty } from 'rxjs';

import * as actions from '../../state/actions';
import * as selectors from "../../state/selectors";
import { SearchState } from '../../state/reducers';
import { ContentModel } from '../../models';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrl: './search.component.sass',
})
export class SearchComponent implements OnInit, OnDestroy {

  contentSubscription: Subscription | null;
  isMedia: boolean = false;
  content: ContentModel[] = [];

  form: FormGroup;

  constructor(
    private store$: Store<any>
  ){
    this.form = new FormGroup(
      {
        search: new FormControl('', [Validators.required, Validators.minLength(3)])
      }
    );
    this.contentSubscription = this.store$.pipe(select(selectors.getContent)).subscribe((content) =>{
      this.content = content;
    })
  }
  ngOnInit(): void {
    
  }

  ngOnDestroy(): void {
    if (!!this.contentSubscription) {
      this.contentSubscription.unsubscribe();
      this.contentSubscription = null;
  }
  }

  isContent(): boolean {
    return this.content.length !== 0  || !this.content
  }

  search() {
    this.isMedia = true;
    if( this.form.valid){
      const data = this.form.get('search')?.value;
      console.log(data)
      this.store$.dispatch(actions.loadContent({query: data}));
    }
  }

}
