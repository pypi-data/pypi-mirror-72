from mnmt.translator import BasicTranslator


class Seq2SeqTranslator(BasicTranslator):

    def __init__(self, quiet_translate):
        """
        Args:
            quiet_translate:  determine whether to print translation or not
        """
        super().__init__(quiet_translate)

    def translate(self, pred, trg, trg_field, output_file=None):
        """
        Args:
            pred:  [batch_size, trg_length], model's output
            trg:  [trg_length, batch_size], target reference
            trg_field:  target language field
            output_file:  save translation results in output_file
        """
        pred = pred[:, 1:]  # [batch_size, trg_length - 1], removing <sos>
        ref = trg[1:].permute(1, 0)  # [batch_size, trg_length - 1]
        return self.matching(pred, ref, trg_field=trg_field,
                             quiet_translate=self.quiet_translate,
                             output_file=output_file)
