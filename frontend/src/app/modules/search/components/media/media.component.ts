import { Component, OnInit, Input } from '@angular/core';
import { Store } from '@ngrx/store';

import { ContentModel } from '../../models';

import * as actions from '../../../../state/actions';

@Component({
  selector: 'app-media',
  templateUrl: './media.component.html',
  styleUrl: './media.component.sass'
})
export class MediaComponent implements OnInit  {

  @Input() content: ContentModel | undefined
  
  constructor(private store$: Store) {}

  ngOnInit() {
  }
}
