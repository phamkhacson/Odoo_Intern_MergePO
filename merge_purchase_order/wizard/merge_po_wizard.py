from odoo import api, models, fields
from odoo.exceptions import UserError


class MergePO(models.TransientModel):
    _name = "merge.po"
    merge_options = fields.Selection([
        ('new_cancel', 'New and cancel all'),
        ('new_delete', 'New and delete all'),
        ('merge_cancel', 'Merge and cancel another one'),
        ('merge_delete', 'Merge and delete another one')
    ], string="Merge Options", default='new_cancel', required=True)
    po_active_id = fields.Many2one('purchase.order', string="Purchase order")

    @api.onchange('merge_options')
    def onchange_merge_options(self):
        res = {}
        for rec in self:
            rec.po_active_id = False
            if rec.merge_options in ['merge_cancel', 'merge_delete']:
                po_ids = self.env['purchase.order'].browse(self._context.get('active_ids', []))
                res['domain'] = {
                    'po_active_id': [('id', 'in', [po.id for po in po_ids])]
                }
            return res

    def merge(self):
        po_ids = self.env['purchase.order'].browse(self._context.get('active_ids', []))
        if len(po_ids) <= 1:
            raise UserError('Must more than 1 po')
        partner = po_ids[0].partner_id.id
        if any(po.partner_id.id != partner for po in po_ids):
            raise UserError('Must be same vendor')
        if any(po.state != 'draft' for po in po_ids):
            raise UserError('Any PO must be RFO')
        if self.merge_options == 'new_cancel':
            new_po = self.env['purchase.order'].create({'partner_id': partner})
            for order in po_ids:
                for line in order.order_line:
                    exiting_order_line = False
                    if new_po.order_line:
                        for new_po_line in new_po.order_line:
                            if new_po_line.product_id == line.product_id and new_po_line.price_unit == line.price_unit:
                                exiting_order_line = new_po_line
                                break
                    if exiting_order_line:
                        exiting_order_line.product_qty += line.product_qty
                        po_taxes = [tax.id for tax in exiting_order_line.taxes_id]
                        for tax in line.taxes_id:
                            po_taxes.append(tax.id)
                        exiting_order_line.taxes_id = [(6, 0, po_taxes)]
                    else:
                        line.copy(default={'order_id': new_po.id})
                order.button_cancel()
        elif self.merge_options == 'new_delete':
            new_po = self.env['purchase.order'].create({'partner_id': partner})
            for order in po_ids:
                for line in order.order_line:
                    exiting_order_line = False
                    if new_po.order_line:
                        for new_po_line in new_po.order_line:
                            if new_po_line.product_id == line.product_id and new_po_line.price_unit == line.price_unit:
                                exiting_order_line = new_po_line
                                break
                    if exiting_order_line:
                        exiting_order_line.product_qty += line.product_qty
                        po_taxes = [tax.id for tax in exiting_order_line.taxes_id]
                        for tax in line.taxes_id:
                            po_taxes.append(tax.id)
                        exiting_order_line.taxes_id = [(6, 0, po_taxes)]
                    else:
                        line.copy(default={'order_id': new_po.id})
            for order in po_ids:
                order.sudo().button_cancel()
                order.sudo().unlink()
        elif self.merge_options == 'merge_cancel':
            po = self.po_active_id
            default = {'order_id': po.id}
            for order in po_ids:
                if order == po:
                    pass
                else:
                    for line in order.order_line:
                        exiting_order_line = False
                        if po.order_line:
                            for po_line in po.order_line:
                                if po_line.product_id == line.product_id and po_line.price_unit == line.price_unit:
                                    exiting_order_line = po_line
                                    break
                        if exiting_order_line:
                            exiting_order_line.product_qty += line.product_qty
                            po_taxes = [tax.id for tax in exiting_order_line.taxes_id]
                            for tax in line.taxes_id:
                                po_taxes.append(tax.id)
                            exiting_order_line.taxes_id = [(6, 0, po_taxes)]
                        else:
                            line.copy(default=default)
            for order in po_ids:
                if order != self.po_active_id:
                    order.button_cancel()
        else:
            po = self.po_active_id
            default = {'order_id': po.id}
            for order in po_ids:
                if order == po:
                    pass
                else:
                    for line in order.order_line:
                        exiting_order_line = False
                        if po.order_line:
                            for po_line in po.order_line:
                                if po_line.product_id == line.product_id and po_line.price_unit == line.price_unit:
                                    exiting_order_line = po_line
                                    break
                        if exiting_order_line:
                            exiting_order_line.product_qty += line.product_qty
                            po_taxes = [tax.id for tax in exiting_order_line.taxes_id]
                            for tax in line.taxes_id:
                                po_taxes.append(tax.id)
                            exiting_order_line.taxes_id = [(6, 0, po_taxes)]
                        else:
                            line.copy(default=default)
            for order in po_ids:
                if order != self.po_active_id:
                    order.sudo().button_cancel()
                    order.sudo().unlink()
