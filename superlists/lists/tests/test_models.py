
from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List

class ItemModelTest(TestCase):

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')


    def test_item_is_related_to_list(self):
        the_list = List.objects.create()
        item = Item()
        item.list = the_list
        item.save()
        self.assertIn(item, the_list.item_set.all())
   
 
    def test_cannot_save_empty_list_items(self):
        the_list = List.objects.create()
        item = Item(list=the_list, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()


    def test_duplicate_items_are_invalid(self):
        the_list = List.objects.create()
        Item.objects.create(list=the_list, text='dupe')
        with self.assertRaises(ValidationError):
            item = Item(list=the_list, text='dupe')
            item.full_clean()


    def test_same_item_can_save_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='copepod')
        item = Item(list=list2, text='copepod')
        item.full_clean()   # should work fine


    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='foo')
        item2 = Item.objects.create(list=list1, text='bar')
        item3 = Item.objects.create(list=list1, text='baz')
        self.assertEqual(
            # per author advice 
            # converting to list is simpler than assertQuerysetEqual?
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    
    def test_list_ordering_again(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='foo')
        item2 = Item.objects.create(list=list1, text='bar')
        item3 = Item.objects.create(list=list1, text='baz')
        self.assertEqual(
            list(list1.item_set.all()),
            [item1, item2, item3]
        )
        

    def test_string_representation(self):
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')



class ListAndItemModelTest(TestCase):

    def test_get_absolute_url(self):
        the_list = List.objects.create()
        self.assertEqual(the_list.get_absolute_url(), '/lists/%d/' % (the_list.id,))
 
