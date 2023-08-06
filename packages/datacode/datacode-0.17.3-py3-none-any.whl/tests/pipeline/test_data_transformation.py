from pandas.testing import assert_frame_equal

from datacode import DataSource, Column
import datacode.hooks as dc_hooks
from tests.pipeline.base import PipelineTest
import tests.test_hooks as th


class TestDataTransformationPipeline(PipelineTest):

    def test_create_and_run_transformation_pipeline_from_func(self):
        dtp = self.create_transformation_pipeline()
        dtp.execute()

        assert_frame_equal(dtp.df, self.expect_func_df)

    def test_create_and_run_transformation_pipeline_from_transform(self):
        dtp = self.create_transformation_pipeline(func=self.source_transform)
        dtp.execute()

        assert_frame_equal(dtp.df, self.expect_loaded_df_with_transform)

    def test_auto_run_pipeline_by_load_source_with_no_location(self):
        dtp = self.create_transformation_pipeline()

        ds = DataSource(pipeline=dtp, location=self.csv_path_output)
        df = ds.df
        assert_frame_equal(df, self.expect_func_df)

    def test_auto_run_pipeline_by_load_source_with_no_location_and_shared_columns(self):
        self.create_csv()
        all_cols = self.create_columns()

        def transform_func(source: DataSource) -> DataSource:
            new_ds = DataSource(df=source.df, columns=all_cols)
            return new_ds

        dtp = self.create_transformation_pipeline(func=transform_func)

        ds = DataSource(pipeline=dtp, location=self.csv_path_output, columns=all_cols)
        df = ds.df
        assert_frame_equal(df, self.expect_loaded_df_rename_only)

    def test_create_nested_transformation_pipeline(self):
        dtp = self.create_transformation_pipeline()

        dtp2 = self.create_transformation_pipeline(source=dtp)
        dtp2.execute()
        assert_frame_equal(dtp2.df, self.expect_df_double_source_transform)

    def test_create_nested_generation_pipeline(self):
        dgp = self.create_generator_pipeline()

        dtp = self.create_transformation_pipeline(source=dgp)
        dtp.execute()

        assert_frame_equal(dtp.df, self.expect_generated_transformed)

    def test_create_nested_merge_pipeline(self):
        dmp = self.create_merge_pipeline()

        dtp = self.create_transformation_pipeline(source=dmp)
        dtp.execute()

        assert_frame_equal(dtp.df, self.expect_merged_1_2_both_transformed)

    def test_original_variables_not_affected_by_transform(self):
        self.create_csv()
        a, b, c = self.create_variables()
        ac = Column(a, 'a')
        bc = Column(b, 'b')
        cc = Column(c, 'c')
        all_cols = [ac, bc, cc]
        source = self.create_source(df=None, columns=all_cols)
        dtp = self.create_transformation_pipeline(source=source)
        dtp.execute()

        assert not a.applied_transforms
        assert not b.applied_transforms
        assert not c.applied_transforms

    def test_transform_on_source_with_normal_and_transformed_of_same_variable(self):
        self.create_csv()
        a, b, c = self.create_variables(transform_data='cell', apply_transforms=False)
        ac = Column(a, 'a')
        bc = Column(b, 'b')
        cc = Column(c, 'c')
        all_cols = [ac, bc, cc]
        include_vars = [
            a,
            a.add_one_cell(),
            b,
            c
        ]
        source = self.create_source(df=None, columns=all_cols, load_variables=include_vars)
        dtp = self.create_transformation_pipeline(source=source)
        dtp.execute()

        assert_frame_equal(dtp.df, self.expect_func_df_with_a_and_a_transformed)

    def test_nested_last_modified(self):
        counter_value = th.COUNTER
        dc_hooks.on_begin_apply_source_transform = th.increase_counter_hook_return_only_second_arg

        dmp = self.create_merge_pipeline()

        dtp = self.create_transformation_pipeline(source=dmp)
        self.create_csv_for_2()
        ds = self.create_source(df=None, location=self.csv_path2, pipeline=dtp)

        # Should not run pipeline as source is newer
        df = ds.df

        dc_hooks.reset_hooks()
        assert_frame_equal(df, self.test_df2)
        assert th.COUNTER == counter_value  # transform operation not called
